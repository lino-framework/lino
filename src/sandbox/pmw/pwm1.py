#
# copied from Pmw_1_2/doc/howtouse.html
#

import Pmw
root=Pmw.initialise(fontScheme='pmw1')

counter=Pmw.Counter(
    label_text='Counter:',
    labelpos='w',
    entryfield_value='00:00:00',
    entryfield_validate='time',
    datatype='time',
    increment=5*60,
)
counter.pack(fill='x', padx=10, pady=10)

entry=Pmw.EntryField(
    label_text='Real entry:',
    labelpos='w',
    value='+2.9979e+8',
    validate='real',
)
entry.pack(fill='x', padx=10, pady=10)

combo=Pmw.ComboBox(
    label_text='ComboBox:',
    labelpos='w',
    scrolledlist_items=map(str, range(20))
)
combo.pack(fill='x', padx=10, pady=10)

# Make the labels line up neatly
Pmw.alignlabels((counter, entry, combo))

root.title('Pmw megawidgets example')
root.mainloop()
