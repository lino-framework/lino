��    �      �  �   	            !     *     =  ?   D  :   �  1   �  +   �  P        n  	   t     ~     �  �   �     %     ,  
   8     C  !   S  
   u     �  	   �     �     �     �     �     �  5   �          &     2     >     E     a  )   }     �  %   �     �     �  	   �  
   �  
                   $  	   )  
   3     >     G     U  �   Z     �     �  	   �  	                  (  	   8     B     H     T     Z  #   c     �     �     �     �  	   �     �     �     �     �  $   �  (        =  9   B     |     �     �     �     �     �  	   �     �     �     �  !   �  '   !  '   I     q  ?   �  )   �     �                 
   &  
   1     <     C    X  F   Z  $   �  )   �  )   �  4     5   O  $   �  |   �  2   '  (   Z  3   �  )   �  5   �  &        >  %   W  j   }     �       U     Q   r  �   �     [     g     t     �     �     �  V   �     �  
          	     
   %     0     6  *   C  .   n     �  I   �  
   �     �  b       e     w     �  �   �  �     |   �  U     w   r     �              	   2   m  <      �!     �!     �!  A   �!  p   8"  "   �"  -   �"     �"     #     ,#  "   I#     l#  D   �#  x   �#  K   J$     �$     �$     �$  @   �$  a   %  �   x%     &  K   -&  0   y&     �&     �&  $   �&     �&  9   '     V'  %   f'     �'     �'     �'     �'  	   (  �  (     �)     �)     �)     *     *  +   +*     W*     w*  %   �*  !   �*     �*  "   �*  z   +     ~+     �+  	   �+  	   �+  "   �+  ,   �+  /   ,  9   ?,     y,  ]   �,  3   �,     -  o   +-  +   �-     �-  5   �-     .     0.  N   M.     �.     �.     �.  L   �.  B   (/  l   k/  8   �/  I   0  �   [0  ]   1     _1     v1     �1  .   �1  "   �1     �1     2  ;   "2  �  ^2  v   W4  N   �4  l   5  i   �5  �   �5  �   �6  R   J7  )  �7  i   �8  [   19  U   �9  ^   �9  �   B:  s   �:  ,   L;  S   y;  Z  �;  G   (=  @   p=  �   �=  �   v>  �  .?  %   �@     A     1A     NA     nA  "   �A  �   �A  !   GB  7   iB     �B  .   �B  .   �B  $   C  "   AC  &   dC  �   �C     D  ;  )D     eE  !   E     �   z             q   �   +                        
          (       J   v       &   �   P   4   ^   ;       s   i      S          )   3       C   6                       -   A       �          \          8   }   w   t   Y   @              =   U       �   /   e   r   '   1      L       W   H           [   u   0          <                  Z   f       V   �   h          n   a   #   j   y   �      G   F       "   �   �   O   �   �   �   :      b          X   �   E       I          M   o       k   .   9           R          7       �   ,   B   {                 |   d             >   l   g   *   �   `      K   2   !   	      ~       p      %   ]       x       �   T       $           5   ?   _          m          Q   c   D   N   �    (object) (of a human)Title (type) A dialog window which displays some information about the site. A pointer to the library volume where this file is stored. A short description entered manually by the user. A space-separated list of all middle names. A virtual field which defines buttons for switching between the
different views. About Act as... Administrator Age Almost the same as description, but if file is
not empty, the text is clickable, and clicking on it opens the
uploaded file in a new browser window. Author Authorities Birth date Change password Change the password of this user. Check data Clear cache Configure Controlled by Created Data checkers Data problems Default build method Defines the Clear cache button on a Printable record. Delete this record Description Designation Detail Displaying {0} - {1} of {2} Duplicate the selected row. Edit help texts for fields on this model. Explorer Export this table as an .xls document Export to .xls Field File size First name First page Fix data problems Gender HTML Help Text Help Texts HelpText Hi, %(user)s! Home If start_date is given, then the user cannot sign in
before that date.  If end_date is given, then the user
cannot sign in after that date. Initials Language Last name Last page Library file Library volume Library volumes MIME type Merge Middle name Model Modified Must be unique and cannot be empty. My settings My {} Myself Name Next page No data to display No data to display. Not used in Lino. Office Open a detail window on this record. Open a dialog window to insert a new {}. Page Pointer to the uploaded file itself (a Django FileField). Previous page Print Print method Quick links: Quick search Rebuild site cache Recipient Refresh Reports Save and close the window. Show a list of all user sessions. Show or hide the table parameters panel Show this table in Bootstrap3 interface Show uploads in a grid table. Shows my uploads (i.e. those whose author is the current user). Shows the list of all users on this site. Sign out Simulated date Site Site Parameters Site owner Start date System Text Field Templates The action used to print this object.
This is an instance of
DirectPrintAction or CachedPrintAction by
default.  And if lino_xl.lib.excerpts is installed,
then set_excerpts_actions possibly replaces
do_print by a
lino_xl.lib.excerpts.CreateExcerpt instance. The author of this object.
A pointer to lino.modlib.users.models.User. The base table for problem messages. The first name, also known as given name. The last name, also known as family name. The list of data checkers known by this application. The list of user types available in this application. The media type of the
uploaded file. The nickname or initials of this user. This does not need to
be unique but should provide a reasonably identifying
function. The path of this file, relative the volume's root. The sex of this person (male or female). The size of the file in bytes. Not yet implemented. The table with all existing upload types. The time when this database object was last modified. The time when this object was created. The type of this upload. The upload area this file belongs to. The user type given to this user. Users having this field empty
are considered inactive and cannot log in. The workflow state field. This is a Lino demo site. Timestamp of the built target file. Contains None
if no build hasn't been called yet. Try also the other <a href="http://lino-framework.org/demos.html">demo sites</a>. Uncomplete dates are allowed, e.g.
"00.00.1980" means "some day in 1980",
"00.07.1980" means "in July 1980"
or "23.07.0000" means "on a 23th of July". Upload area Upload areas Upload files Upload type Upload types Uploaded by Used to specify a professional position or academic
qualification like "Dr." or "PhD". User User roles User sessions User type User types Users Verbose name Virtual field displaying the age in years. We are running with simulated date set to {0}. Workflow Your feedback is welcome to %s or directly to the person who invited you. build time of {0} Project-Id-Version: lino 21.3.0
Report-Msgid-Bugs-To: EMAIL@ADDRESS
PO-Revision-Date: 2021-03-12 19:05+0600
Last-Translator: 
Language: bn
Language-Team: bn <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.9.0
X-Generator: Poedit 2.4.2
 (বস্তু) শিরোনাম (ধরন) সাইট সংক্রান্ত কিছু সাধারন তথ্যের ডায়ালগ উইনডো। নথিশালার পথ নির্দেশ করে যেখানে এই ফাইলটি জমা আছে। ব্যবহারকারীর ম্যানুয়ালি সমার্পিত ছোট বর্ণনা। নামের সকল মধ্যাংশ গুলোর তালিকা। ভিন্ন চিত্রের ছকে পরিবর্তনের কৃত্রিম বোতাম। প্রামাণ্য ভূমিকা... পরিচালক বয়স পূর্বে দেখা বর্ণনার মতই, কিন্তু যদি ফাইলটি
ফাঁকা না হয় তবে এই বর্ণনাতে ক্লিক করলে ফাইলটির বিস্তারিত নতুন
একটি ব্রাউজার উইন্ডোতে ওপেন হবে। রচয়িতা কর্তৃপক্ষ জন্ম তারিখ পাসওয়ার্ড পরিবর্তন করুন এই ব্যবহারকারীর পাসওয়ার্ড পরিবর্তন করুন। তথ্য পরিক্ষা কেশ (cache) মুছেফেলুন কনফিগার নিয়ন্ত্রক প্রণয়ন কাল তথ্য পরীক্ষক তথ্য সমস্যা সাধারন নির্মাণ প্রক্রিয়া প্রিন্ট করার মত শারি গুলোর কেশ (cache) মুছে ফেলুন। বাছাইকৃত শারিটি মুছে ফেলুন। বর্ণনা আখ্যা বিস্তারিত {2} শারির মধ্যে দেখছেন {0} - {1} বাছাইকৃত শারির প্রতিলিপি তৈরি করুন। এই ছকের উপাদান গুলোর সম্বন্ধ সহায়ক বাক্যে পরিবর্তন আনুন। অনুসন্ধান এই ছকটি .xls (এক্সেল) এ বের করুন। এক্সেল (.xls) বের করুন ক্ষেত্র ফাইল সাইজ নাম (প্রথমাংশ) প্রথম পাতা তথ্য সমস্যা ঠিক করুন। লিঙ্গ এইচ টি এম এল (HTML) সহায়ক বাক্য সহায়ক বাক্য সহায়ক বাক্য হাই, %(user)s! হোম যদি সূচনা কাল (start_date) দেয়া হয়ে থাকে তবে এর ব্যবহারকারী
এই দিনের পূর্বে লগইন করতে পারবে না। যদি শেষ কাল (end_date)
দেয়া হয়ে থাকে তবে এর ব্যবহারকারী এই দিনের পর লগইন করতে পারবে না। ডাক নাম ভাষা নাম (শেষাংশ) শেষ পাতা নথি বই লাইব্রেরী ভলিউম গ্রন্থ খন্ড মাইম (MIME) একত্রিত করুন। নাম (মধ্যাংশ) মডেল পরিবর্তন কাল অবশ্যই অদ্বিতীয় হতে হবে এবং খালি হতে পারবে না। আমার সেটিং আমার {} আমি নাম পরবর্তী পাতা দেখার কিছু নেই (^_^) দেখার কিছু নেই (^_^)। লিনোতে ব্যবহার হয় না। অফিস বাছাইকৃত শারিটির বিস্তারিত দেখুন। ছকে নতুন {} যোগ করুন। পৃষ্ঠা আপলোড করা ফাইলটি নির্দেশ করে (একটি Django FileField)। পূর্ববর্তী পাতা প্রিন্ট প্রিন্ট করার মাধ্যম কুইক লিংকঃ কুইক সার্চ সাইট কেশ (cache) আবার নির্মাণ করুন প্রাপক রিফ্রেশ রিপোর্ট সংরক্ষণ শেষে ছকটি বন্ধ করুন। সকল ইউজার সেশনের তালিকা। ছকের পরামিতি প্যানেল খুলুন বা বন্ধ করুন। এই ছকটি Bootstrap3 তে দেখুন। গ্রিড ছকে আপলোড গুলো দেখুন। আমার আপলোড সমূহ (i.e. ওগুলো, যেগুলোর রচয়িতা বর্তমান ব্যবহারকারী)। সাইটের সকল ব্যবহারকারীদের তালিকা। সাইন আউট অনুকৃত দিন সাইট সাইট প্যারামিটার সাইটের মালিক সূচনা কাল সিস্টেম টেক্সট ফিল্ড টেম্পলেট যেকোনো শারি প্রিন্ট করার জন্য ব্যবহারিত একশন।
সাধারণ ভাবে এটি DirectPrintAction অথবা
CachedPrintAction এর একটি instance।
এবং যদি lino_xl.lib.excerpts ইন্সটল করা থাকে তবে
এটা সম্ভব যে set_excerpts_actions do_print কে
lino_xl.lib.excerpts.CreateExcerpt instance দিয়ে
পরিবর্তন করে। এই বস্তুটির রচয়িতা।
lino.modlib.users.models.User নির্দেশ করে। সমস্যা সংক্রান্ত বার্তার ছক। নামের প্রথমাংশ, দেয়া নাম হিসেবেও পরিচিত। নামের শেষাংশ, বংশীও নাম হিসেবেও পরিচিত। এই অ্যাপ্লিকেশনের অন্তর্ভুক্ত সকল তথ্য পরীক্ষকের তালিকা। এই অ্যাপ্লিকেশনে অন্তর্ভুক্ত সকল প্রকার ব্যবহারকারীর ধরনের তালিকা। আপলোড করা ফাইলটির
মিডিয়ার ধরন। ব্যবহারকারীর ডাক নাম। এটি অদ্বিতীয় হতে হবে না কিন্তু ব্যবহারকারীকে
যুক্তিসঙ্গত ভাবে চিহ্নিত করতে কর্যকরি হবে। ভলিউম রুট থেকে এই ফাইলটির আপেক্ষিক পাথ। এই লোকটির লিঙ্গভেদ (পুরুষ বা নারী)। ফাইলটির সাইজ (bytes). এখনো সক্রিয় নয়। সম্ভব্য আপলোডের ধরন সমূহের তালিকা। যে সময় এই ডাটাবেইজ-বস্তুটি সর্বশেষ পরিবর্তন করা হয়েছিল। যে সময় এই ডাটাবেইজ-বস্তুটি তৈরি করা হয়েছিল। এই আপলোডটির ধরন। এই আপলোড করা ফাইলটি যে অঞ্চলের। ব্যবহারকারীকে দেয়া ব্যবহারকারীর-ধরন। যে ব্যবহারকারীর এই ক্ষেত্রটি খালি
তাকে নিষ্ক্রিয় বিবেচনা করা হবে এবং সে লগইন করতে পারবে না। কর্মধারার বর্তমান অবস্থা। এটি একটি লিনো ডেমো সাইট। উল্লেখ্য ফাইল তৈরির টাইমস্ট্যাম্প। None থাকবে
যদি কোন ফাইল তৈরি হয়ে না থাকে। চাইলে, অন্যান্য <a href="http://lino-framework.org/demos.html">ডেমো সাইট</a> গুলো-ও ঘুরে দেখতে পারেন। অসম্পূর্ণ দিনও গ্রহণযোগ্য, যেমন,
"০০.০০.১৯৮০" মানে, ১৯৮০ সালের যেকোনো দিন,
"০০.০৭.১৯৮০" মানে, ১৯৮০ সালের জুলাই মাসের যেকোনো দিন,
অথবা "২৩.০৭.০০০০" মানে যেকোনো বছরের ২৩শে জুলাই। আপলোডের অঞ্চল স্থান আপলোড ফাইল আপলোড আপলোডের ধরন আপলোডের ধরন আপলোড করেছেন পেশাগত বা একাডেমীক পদ বুঝাতে ব্যবহার হয়।
যেমন, "Dr" অথবা "PhD"। ব্যবহারকারী ব্যবহারকারীর ভূমিকা ইউজার সেশন ব্যবহারকারীর ধরন ব্যবহারকারীর ধরন ব্যাবহারকারী শব্দবহুল নাম বছর গণনায় বয়স। আমরা কৃত্রিম দিনক্ষণ {0} -এ আমাদের যাত্রা শুরু করছি। কর্মধারা এই সাইটের ব্যাপারে %s -এ অথবা যার মাধ্যমে আমাদের খোঁজ পেয়েছেন তার নিকট আপনার প্রতিক্রিয়া আমাদের নিকট খুবই গুরুত্বপূর্ণ। তৈরির সময় মোট {0} টি থেকে 