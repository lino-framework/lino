/*global module:false*/
module.exports = function(grunt) {

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        meta: {
            banner: '/**\n' +
                ' * <%= pkg.description %>\n' +
                ' * @version v<%= pkg.version %> - <%= grunt.template.today("yyyy-mm-dd") %>\n' +
                ' * @link <%= pkg.homepage %>\n' +
                ' * @author <%= pkg.author %>\n' +
                ' * @license MIT License, http://www.opensource.org/licenses/MIT\n' +
                ' */\n'
        },
        clean: {
            js: ['openui5']
        },
        dirs: {
            src: 'src/*.js',
            dest: 'openui5'
        },
        concat: {
            options: {
                banner: '<%= meta.banner %>'
            },
            basic: {
                src: ['src/ckeditor-dbg.js', 'src/CKEditorToolbar.js'],
                dest: '<%= dirs.dest %>/ckeditor.js'
            },
            debug: {
                src: ['openui5/ckeditor-dbg.js'],
                dest: 'openui5/ckeditor-dbg.js',
            },
            config: {
                src: ['openui5/CKEditorToolbar.js'],
                dest: 'openui5/CKEditorToolbar.js',
            },
        },
        uglify: {
            options: {
                banner: '<%= meta.banner %>'
            },
            dist: {
                src: ['<%= dirs.dest %>/ckeditor.js'],
                dest: '<%= dirs.dest %>/ckeditor.js'
            }
        },
        jshint: {
            files: ['Gruntfile.js', '<%= dirs.src %>'],
            options: {
                "devel": true,
                "curly": true,
                "eqeqeq": true,
                "immed": true,
                "latedef": true,
                "newcap": true,
                "noarg": true,
                "sub": true,
                "undef": true,
                "unused": false,
                "boss": true,
                "eqnull": true,
                "browser": true,
                "globals": {
                    "jQuery": true,
                    "sap": true,
                    "$": true,
                    "util": true,
                    "view": true,
                    "model": true
                }
            }
        },
        copy: {
            main: {
                files: [{
                    expand: true,
                    src: 'src/*',
                    dest: 'openui5/',
                    flatten: true
                }]
            }
        },
        connect: {
            options: {
                keepalive: true
            },
            server: {}
        }
    });

    grunt.registerTask('default', ['build']);

    grunt.registerTask('build', ['jshint', 'copy', 'concat', 'uglify']);

};