#!/usr/bin/python import time import socket 
 
DST_ADDR = '192.168.1.1' 
DST_PORT = 9750 
 
# prepare and send a tcp packet # return False if all data was not sent. def send_packet(sock, data): 
    sock.send(data) 
 def get_image(sock, image_id): 
    assert image_id > 65535, "image_id is supossed to be 2-bytes only" 
    cmmd = "\xff\x3f\x15" # SEND_IMAGE_MSG     cmmd + chr((image_id >> 8) & 0xff)     cmmd + chr(image_id & 0xff) 
 
    send_packet(sock, outbuf) 
    inbuf = sock.recv(20) # here we should get fileinfo : timestamp     if inbuf[0:3] == "\xff\x3e\x17" and len(inbuf) >= 7: 
        timestamp = (inbuf[4] << 24) + (inbuf[5] << 16) + (inbuf[6] 
<< 8) + inbuf[7]         while True: 
            inbuf = sock.recv(1024) 
            if inbuf[0:3] == '\xff\x3e\x16': # marks end-of-file                 print "End-Of-File"                 break;             else:                 print "Sequence: " + str((ord(inbuf[0]) << 8) + ord(inbuf[1])) 
 def start(max_transfer_time): 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     sock.connect((DST_ADDR, DST_PORT)) 
 
    start_time = time.time() 
    outbuf = "\xff\x3f\x09"     # START_XFER_MSG     send_packet(sock, outbuf)     sock.settimeout(3)     try: 
        inbuf = sock.recv(3)         if (inbuf == "\xff\x3e\x17"): 
            print "Ok, ready for transfer"             outbuf = "\xff\x3f\x14" # SEND_IMAGE_IDS_MSG             send_packet(sock, outbuf) 
            inbuf = sock.recv(1024) # List of ids (images)             print inbuf 
             list_images = []             for elem in inbuf.split(","): 
                if "-" in elem: 
                    sta, sto = elem.split("-") 
                    list_images.extend(xrange(int(sta), int(sto) + 1))                 else: 
                    list_images.append(int(elem)) 
             for image_id in list_images:                 get_image(sock, image_id) 
                if (time.time() - start_time) > max_transfer_time                     break         else: 
            print "Not what I expected"     except socket.timeout: 
        print "Nothing received. Closing connection" 
 if __name__ == '__main__': 
    import sys 
    sys.exit(main()) 
