LINUX
gcc -shared -o "key_tracker_x86_64.so" -I "/usr/local/include/python3.11/" -fPIC "/key_tracker_c/key_tracker.c"

WINDOWS
cl /LD /I"C:/Program Files/Python311/include"  "./key_tracker_c/key_tracker.c" /link /LIBPATH:"C:/Program Files/Python311/libs" /OUT:key_tracker_x64.pyd

cl /LD /I"C:/Program Files (x86)/Python311-32/include" "key_tracker_c/key_tracker.c" /link /LIBPATH:"C:/Program Files (x86)/Python311-32/libs"  /OUT:key_tracker_x86.pyd


cl /LD /I"D:/Programme/Python310/include"  "./key_tracker_c/key_tracker.c" /link /LIBPATH:"D:/Programme/Python310/libs" /OUT:key_tracker_x64.pyd