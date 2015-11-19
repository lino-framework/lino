=================================
Tuning MySQL database performance
=================================

This section is for tuning a MySQL server which is already installed.
See also :doc:`install_mysql`.

.. contents:: Table of contents
    :local:
    :depth: 1

.. _innodb:

Lino and the InnoDB engine
==========================

Lino versions before :blogref:`20141220` were more easy to use with
the MyISAM storage instead of the default InnoDB storage (see `Setting
the Storage Engine
<http://dev.mysql.com/doc/refman/5.1/en/storage-engine-setting.html>`_).

Using InnoDB could cause
the following error message when trying to run :manage:`initdb` on a
non-empty database::

    IntegrityError: (1217, 'Cannot delete or update a parent row: 
    a foreign key constraint fails')

This was because :manage:`initdb` could fail to drop tables due to
InnoDB's more severe integrity contraints.

Even with InnoDB it was possible to work around this problem by doing
yourself a `DROP DATABASE` followed by a new `CREATE DATABASE` each
time before running :manage:`initdb`.

.. _mysql.engine:

MyISAM or InnoDB?
=================

The `storage engine
<http://dev.mysql.com/doc/refman/5.1/en/storage-engine-setting.html>`_
(typically either MyISAM or InnoDB, see also `Comparison of MySQL
database engines
<https://en.wikipedia.org/wiki/Comparison_of_MySQL_database_engines>`_)
can influence your database performance.


To set the default storage engine to InnoDB, add an `init_command`
option to your database setting::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            ...
            'OPTIONS': {
                "init_command": "SET storage_engine=MyISAM",
            }
        },
    }

Alternatively you can set the *system-wide* default database storage
on a Debian server by creating a file
:file:`/etc/mysql/conf.d/set_myisam_engine.cnf` with this content::

    [mysqld]
    default-storage-engine=myisam

Instead of naming the file :file:`set_myisam_engine.cnf`, you might
consider naming it :file:`.keepme`.


MySQLTuner
==========

Use `MySQLTuner-perl <https://github.com/major/mysqltuner-perl>`_ to
analyze Lino's database usage::

  $ wget https://raw.githubusercontent.com/major/MySQLTuner-perl/master/mysqltuner.pl
  $ perl mysqltuner.pl

Example output::

    Please enter your MySQL administrative login: django
    Please enter your MySQL administrative password: 
    [OK] Currently running supported MySQL version 5.5.41-0+wheezy1-log
    [OK] Operating on 64-bit architecture

    -------- Storage Engine Statistics -------------------------------------------
    [--] Status: +ARCHIVE +BLACKHOLE +CSV -FEDERATED +InnoDB +MRG_MYISAM 
    [--] Data in MyISAM tables: 1M (Tables: 162)
    [!!] InnoDB is enabled but isn't being used
    [!!] Total fragmented tables: 2

    -------- Security Recommendations  -------------------------------------------
    ERROR 1142 (42000) at line 1: SELECT command denied to user 'django'@'localhost' for table 'user'
    [OK] All database users have passwords assigned

    -------- Performance Metrics -------------------------------------------------
    [--] Up for: 50m 29s (1M q [433.129 qps], 4K conn, TX: 813M, RX: 937M)
    [--] Reads / Writes: 98% / 2%
    [--] Total buffers: 192.0M global + 2.7M per thread (151 max threads)
    [OK] Maximum possible memory usage: 597.8M (3% of installed RAM)
    [OK] Slow queries: 0% (643/1M)
    [OK] Highest usage of available connections: 10% (16/151)
    [OK] Key buffer size / total MyISAM indexes: 16.0M/2.7M
    [OK] Key buffer hit rate: 99.9% (1M cached / 679 reads)
    [OK] Query cache efficiency: 99.4% (1M cached / 1M selects)
    [OK] Query cache prunes per day: 0
    [OK] Sorts requiring temporary tables: 0% (0 temp sorts / 566 sorts)
    [!!] Joins performed without indexes: 99
    [OK] Temporary tables created on disk: 17% (365 on disk / 2K total)
    [OK] Thread cache hit rate: 98% (79 created / 4K connections)
    [OK] Table cache hit rate: 26% (223 open / 839 opened)
    [OK] Open file limit used: 38% (393/1K)
    [OK] Table locks acquired immediately: 100% (13K immediate / 13K locks)

    -------- Recommendations -----------------------------------------------------
    General recommendations:
        Add skip-innodb to MySQL configuration to disable InnoDB
        Run OPTIMIZE TABLE to defragment tables for better performance
        MySQL started within last 24 hours - recommendations may be inaccurate
        Adjust your join queries to always utilize indexes
    Variables to adjust:
        join_buffer_size (> 128.0K, or always use indexes with joins)



Which tables are fragmented?
============================

Short answer (thanks to `Felipe Rojas <http://serverfault.com/questions/202000/how-find-and-fix-fragmented-mysql-tables>`_)::

    mysql> select  ENGINE, TABLE_NAME, Round( DATA_LENGTH/1024/1024) as data_length , round(INDEX_LENGTH/1024/1024) as index_length, round(DATA_FREE/ 1024/1024) as data_free from information_schema.tables  where  DATA_FREE > 0;

Sample result::

    +--------+-----------------------+-------------+--------------+-----------+
    | ENGINE | TABLE_NAME            | data_length | index_length | data_free |
    +--------+-----------------------+-------------+--------------+-----------+
    | MyISAM | courses_coursecontent |           0 |            0 |         0 |
    | MyISAM | polls_response        |           0 |            0 |         0 |
    +--------+-----------------------+-------------+--------------+-----------+
    2 rows in set (0.01 sec)


mysqldumpslow
=============

Here is my cheat sheet (thanks to `rtCamp Solutions
<https://rtcamp.com/tutorials/mysql/slow-query-log/>`_)::

  $ sudo nano /etc/mysql/my.cnf  # uncomment lines around "slow-query-log"
  $ sudo /etc/init.d/mysql restart

  $ sudo mysqldumpslow -a -s r -t 5  /var/log/mysql/mysql-slow.log
  $ sudo mysqldumpslow -a -s c -t 5  /var/log/mysql/mysql-slow.log

  $ sudo nano /etc/mysql/my.cnf  # comment lines around "slow-query-log"
  $ sudo /etc/init.d/mysql restart


Example output (``-s c`` : top 5 by count)::

    Reading mysql slow query log from /var/log/mysql/mysql-slow.log
    Count: 19  Time=0.00s (0s)  Lock=0.00s (0s)  Rows=6.0 (114), django[django]@localhost
      SELECT DISTINCT `cal_event`.`id`, `cal_event`.`modified`, `cal_event`.`created`, `cal_event`.`project_id`, `cal_event`.`build_time`, `cal_event`.`build_method`, `cal_event`.`user_id`, `cal_event`.`owner_type_id`, `cal_event`.`owner_id`, `cal_event`.`start_date`, `cal_event`.`start_time`, `cal_event`.`end_date`, `cal_event`.`end_time`, `cal_event`.`summary`, `cal_event`.`description`, `cal_event`.`access_class`, `cal_event`.`sequence`, `cal_event`.`auto_type`, `cal_event`.`event_type_id`, `cal_event`.`transparent`, `cal_event`.`room_id`, `cal_event`.`priority_id`, `cal_event`.`state`, `cal_event`.`assigned_to_id` FROM `cal_event` INNER JOIN `cal_guest` ON ( `cal_event`.`id` = `cal_guest`.`event_id` ) WHERE (`cal_event`.`user_id` = 4  AND `cal_guest`.`state` = '45' )

    Count: 19  Time=0.01s (0s)  Lock=0.00s (0s)  Rows=4.0 (76), django[django]@localhost
      SELECT `cal_event`.`id`, `cal_event`.`modified`, `cal_event`.`created`, `cal_event`.`project_id`, `cal_event`.`build_time`, `cal_event`.`build_method`, `cal_event`.`user_id`, `cal_event`.`owner_type_id`, `cal_event`.`owner_id`, `cal_event`.`start_date`, `cal_event`.`start_time`, `cal_event`.`end_date`, `cal_event`.`end_time`, `cal_event`.`summary`, `cal_event`.`description`, `cal_event`.`access_class`, `cal_event`.`sequence`, `cal_event`.`auto_type`, `cal_event`.`event_type_id`, `cal_event`.`transparent`, `cal_event`.`room_id`, `cal_event`.`priority_id`, `cal_event`.`state`, `cal_event`.`assigned_to_id` FROM `cal_event` INNER JOIN `cal_eventtype` ON ( `cal_event`.`event_type_id` = `cal_eventtype`.`id` ) WHERE (`cal_event`.`user_id` = 3  AND `cal_eventtype`.`is_appointment` = 1  AND `cal_event`.`start_date` >= '2015-03-06' ) ORDER BY `cal_event`.`start_date` ASC, `cal_event`.`start_time` ASC LIMIT 15

    Count: 18  Time=0.00s (0s)  Lock=0.00s (0s)  Rows=1.0 (18), django[django]@localhost
      SELECT COUNT(*) FROM `cal_guest` INNER JOIN `cal_event` ON ( `cal_guest`.`event_id` = `cal_event`.`id` ) WHERE (`cal_event`.`user_id` = 4  AND `cal_guest`.`waiting_since` < '2015-03-06 10:44:00'  AND `cal_guest`.`state` = '44' )

    Count: 16  Time=0.00s (0s)  Lock=0.00s (0s)  Rows=1.0 (16), django[django]@localhost
      SELECT COUNT(DISTINCT `cal_event`.`id`) FROM `cal_event` INNER JOIN `cal_guest` ON ( `cal_event`.`id` = `cal_guest`.`event_id` ) WHERE (`cal_event`.`user_id` = 4  AND `cal_guest`.`state` = '45' )

    Count: 16  Time=0.00s (0s)  Lock=0.00s (0s)  Rows=1.0 (16), django[django]@localhost
      SELECT COUNT(*) FROM `cal_guest` INNER JOIN `cal_event` ON ( `cal_guest`.`event_id` = `cal_event`.`id` ) WHERE (`cal_event`.`user_id` = 27  AND `cal_guest`.`waiting_since` < '2015-03-06 09:23:44'  AND `cal_guest`.`state` = '44' )

Example output (``-s r`` : top 5 by request time)::

    Count: 8  Time=0.02s (0s)  Lock=0.00s (0s)  Rows=2395.1 (19161), django[django]@localhost
      SELECT `pcsw_client`.`person_ptr_id` FROM `pcsw_client` INNER JOIN `contacts_person` ON ( `pcsw_client`.`person_ptr_id` = `contacts_person`.`partner_ptr_id` ) INNER JOIN `contacts_partner` ON ( `contacts_person`.`partner_ptr_id` = `contacts_partner`.`id` ) WHERE (`contacts_partner`.`is_obsolete` = 0  AND `pcsw_client`.`client_state` = '30' ) ORDER BY `contacts_person`.`last_name` ASC, `contacts_person`.`first_name` ASC, `pcsw_client`.`person_ptr_id` ASC

    Count: 3  Time=0.04s (0s)  Lock=0.00s (0s)  Rows=2464.0 (7392), django[django]@localhost
      SELECT DISTINCT `pcsw_client`.`person_ptr_id`, `contacts_person`.`last_name`, `contacts_person`.`first_name` FROM `pcsw_client` INNER JOIN `contacts_person` ON ( `pcsw_client`.`person_ptr_id` = `contacts_person`.`partner_ptr_id` ) INNER JOIN `contacts_partner` ON ( `contacts_person`.`partner_ptr_id` = `contacts_partner`.`id` ) LEFT OUTER JOIN `pcsw_coaching` ON ( `pcsw_client`.`person_ptr_id` = `pcsw_coaching`.`client_id` ) WHERE (`contacts_partner`.`is_obsolete` = 0  AND (`pcsw_coaching`.`end_date` IS NULL OR `pcsw_coaching`.`end_date` >= '2015-03-06' ) AND `pcsw_coaching`.`start_date` <= '2015-03-06'  AND `pcsw_client`.`client_state` IN ('30', '10')) ORDER BY `contacts_person`.`last_name` ASC, `contacts_person`.`first_name` ASC, `pcsw_client`.`person_ptr_id` ASC

    Count: 1  Time=0.11s (0s)  Lock=0.00s (0s)  Rows=2394.0 (2394), django[django]@localhost
      SELECT T5.`id`, T5.`modified`, T5.`created`, T5.`country_id`, T5.`city_id`, T5.`zip_code`, T5.`region_id`, T5.`addr1`, T5.`street_prefix`, T5.`street`, T5.`street_no`, T5.`street_box`, T5.`addr2`, T5.`name`, T5.`language`, T5.`email`, T5.`url`, T5.`phone`, T5.`gsm`, T5.`fax`, T5.`remarks`, T5.`is_obsolete`, T5.`activity_id`, T5.`client_contact_type_id`, T4.`partner_ptr_id`, T4.`first_name`, T4.`middle_name`, T4.`last_name`, T4.`gender`, T4.`birth_date`, T4.`title`, `pcsw_client`.`person_ptr_id`, `pcsw_client`.`national_id`, `pcsw_client`.`nationality_id`, `pcsw_client`.`card_number`, `pcsw_client`.`card_valid_from`, `pcsw_client`.`card_valid_until`, `pcsw_client`.`card_type`, `pcsw_client`.`card_issuer`, `pcsw_client`.`noble_condition`, `pcsw_client`.`group_id`, `pcsw_client`.`birth_place`, `pcsw_client`.`birth_country_id`, `pcsw_client`.`civil_state`, `pcsw_client`.`residence_type`, `pcsw_client`.`in_belgium_since`, `pcsw_client`.`residence_until`, `pcsw_client`.`unemployed_since`, `pcsw_client`.`needs_residence_permit`, `pcsw_client`.`needs_work_permit`, `pcsw_client`.`work_permit_suspended_until`, `pcsw_client`.`aid_type_id`, `pcsw_client`.`declared_name`, `pcsw_client`.`is_seeking`, `pcsw_client`.`unavailable_until`, `pcsw_client`.`unavailable_why`, `pcsw_client`.`obstacles`, `pcsw_client`.`skills`, `pcsw_client`.`job_office_contact_id`, `pcsw_client`.`client_state`, `pcsw_client`.`refusal_reason`, `pcsw_client`.`sis_motif`, `pcsw_client`.`sis_attentes`, `pcsw_client`.`sis_moteurs`, `pcsw_client`.`sis_objectifs`, `pcsw_client`.`oi_demarches`, `pcsw_client`.`geographic_area`, `pcsw_client`.`child_custody`, `pcsw_client`.`broker_id`, `pcsw_client`.`faculty_id`, `countries_country`.`name`, `countries_country`.`isocode`, `countries_country`.`short_code`, `countries_country`.`iso3`, `countries_country`.`name_nl`, `countries_country`.`inscode`, `countries_place`.`id`, `countries_place`.`name`, `countries_place`.`country_id`, `countries_place`.`zip_code`, `countries_place`.`type`, `countries_place`.`parent_id`, `countries_place`.`name_nl`, `countries_place`.`inscode` FROM `pcsw_client` INNER JOIN `contacts_person` ON ( `pcsw_client`.`person_ptr_id` = `contacts_person`.`partner_ptr_id` ) INNER JOIN `contacts_partner` ON ( `contacts_person`.`partner_ptr_id` = `contacts_partner`.`id` ) INNER JOIN `contacts_person` T4 ON ( `pcsw_client`.`person_ptr_id` = T4.`partner_ptr_id` ) INNER JOIN `contacts_partner` T5 ON ( T4.`partner_ptr_id` = T5.`id` ) LEFT OUTER JOIN `countries_country` ON ( `contacts_partner`.`country_id` = `countries_country`.`isocode` ) LEFT OUTER JOIN `countries_place` ON ( `contacts_partner`.`city_id` = `countries_place`.`id` ) WHERE (`contacts_partner`.`is_obsolete` = 0  AND `pcsw_client`.`client_state` = '30' ) ORDER BY `contacts_person`.`last_name` ASC, `contacts_person`.`first_name` ASC, `pcsw_client`.`person_ptr_id` ASC

    Count: 15  Time=0.00s (0s)  Lock=0.00s (0s)  Rows=15.0 (225), django[django]@localhost
      SELECT `cal_event`.`id`, `cal_event`.`modified`, `cal_event`.`created`, `cal_event`.`project_id`, `cal_event`.`build_time`, `cal_event`.`build_method`, `cal_event`.`user_id`, `cal_event`.`owner_type_id`, `cal_event`.`owner_id`, `cal_event`.`start_date`, `cal_event`.`start_time`, `cal_event`.`end_date`, `cal_event`.`end_time`, `cal_event`.`summary`, `cal_event`.`description`, `cal_event`.`access_class`, `cal_event`.`sequence`, `cal_event`.`auto_type`, `cal_event`.`event_type_id`, `cal_event`.`transparent`, `cal_event`.`room_id`, `cal_event`.`priority_id`, `cal_event`.`state`, `cal_event`.`assigned_to_id` FROM `cal_event` INNER JOIN `cal_eventtype` ON ( `cal_event`.`event_type_id` = `cal_eventtype`.`id` ) WHERE (`cal_event`.`user_id` = 19  AND `cal_eventtype`.`is_appointment` = 1  AND `cal_event`.`start_date` >= '2015-03-06' ) ORDER BY `cal_event`.`start_date` ASC, `cal_event`.`start_time` ASC LIMIT 15

    Count: 1  Time=0.01s (0s)  Lock=0.00s (0s)  Rows=193.0 (193), debian-sys-maint[debian-sys-maint]@localhost
      select concat('select count(*) into @discard from `',
      TABLE_SCHEMA, '`.`', TABLE_NAME, '`') 
      from information_schema.TABLES where ENGINE='MyISAM'



