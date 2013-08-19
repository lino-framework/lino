/*
* See http://lino-framework.org/eid/index.html
* 
* Copyright 2013 Luc Saffre
* This file is part of the Lino project.
* Lino is free software; you can redistribute it and/or modify 
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 3 of the License, or
* (at your option) any later version.
* Lino is distributed in the hope that it will be useful, 
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
* GNU General Public License for more details.
* You should have received a copy of the GNU General Public License
* along with Lino; if not, see <http://www.gnu.org/licenses/>.
*
* 
* This is largely inspired by 
* http://blog.codeborne.com/2010/10/javaxsmartcardio-and-esteid.html
* 
*/

package lino.eid;

import java.applet.Applet;
import java.security.Permission;

import java.io.FilePermission;
import java.io.UnsupportedEncodingException;  

import java.util.Arrays;  
import java.util.List; 

import javax.smartcardio.CardPermission;  
import javax.smartcardio.CardChannel;  
import javax.smartcardio.CardException;  
import javax.smartcardio.CommandAPDU;  
import javax.smartcardio.ResponseAPDU;  
import javax.smartcardio.TerminalFactory;  
import javax.smartcardio.CardTerminal;  
import javax.smartcardio.Card;  
import javax.smartcardio.ATR;  

//~ import lino.eid.EidReaderResponse;  
  
//~ import javax.smartcardio.*;  
  
//~ import static ee.esteid.EstEIDUtil.bytesToString;  
//~ import static ee.esteid.EstEIDUtil.sendCommand;  
  
  
class EstEIDUtil {  
  static String ENCODING = "windows-1252";  
  
  public static String bytesToString(byte[] data) {  
    try {  
      return new String(data, ENCODING);  
    } catch (UnsupportedEncodingException e) {  
      throw new RuntimeException("Encoding " + ENCODING + " not supported");  
    }  
  }  
  
  public static byte[] sendCommand(CardChannel channel, CommandAPDU command) throws CardException {  
    ResponseAPDU responseAPDU = channel.transmit(command);  
    int responseStatus = responseAPDU.getSW();  
  
    if (!isResponseOk(responseStatus)){  
      throw new RuntimeException("Error code: " + responseStatus);  
    }  
      
    return responseAPDU.getData();  
  }  
  
  private static boolean isResponseOk(int responseStatus){  
    return responseStatus == 0x9000;  
  }  
} 


  
class PersonalFile {  
  String[] data = new String[16];  
  public static final  CommandAPDU SELECT_MASTER_FILE = new CommandAPDU(
    new byte[]{0x00, (byte)0xA4, 0x00, 0x0C});  
  public static final CommandAPDU SELECT_FILE_EEEE = new CommandAPDU(
    new byte[]{0x00, (byte)0xA4, 0x01, 0x0C, 0x02, (byte)0xEE, (byte)0xEE});  
  public static final CommandAPDU SELECT_FILE_5044 = new CommandAPDU(
    new byte[]{0x00, (byte)0xA4, 0x02, 0x04, 0x02, (byte)0x50, (byte)0x44});  
  public static final String[] fields = new String[] {
      "last_name","first_name", "other_names", "gender", "nationality",
      "birth_date","national_id","card_id","valid_until",
      "birth_place", "date_issued", "ResidencePermitType",
      "remark1",
      "remark2",
      "remark3",
      "remark4"
      };
  
  public PersonalFile(CardChannel channel) throws CardException {  
    init(channel);  
  }  
  
  @Override  
  public String toString() {  
    String s = "";
    for (byte i = 0; i < 16; i++) {  
        s = s + fields[i] + ":" + data[i].trim() + "\n";
    }
    return s;
  }  
  
  private void init(CardChannel channel) throws CardException {  
    EstEIDUtil.sendCommand(channel, SELECT_MASTER_FILE);  
    EstEIDUtil.sendCommand(channel, SELECT_FILE_EEEE);  
    EstEIDUtil.sendCommand(channel, SELECT_FILE_5044);  
  
    for (byte i = 1; i <= 16; i++) {  
      data[i - 1] = extractField(channel, i);  
    }  
  }  
  
  private String extractField(CardChannel channel, byte fieldNumber) throws CardException {  
    return EstEIDUtil.bytesToString(
        EstEIDUtil.sendCommand(channel, 
            new CommandAPDU(new byte[]{0x00, (byte)0xB2, fieldNumber, 0x04, 0x00})));  
  }  
}  


public class EIDReader extends Applet {
//~ class EstEID {
      
    public void unused_init() {
        System.err.println("Gonna disable the security manager...");
        System.setSecurityManager(null);
        System.err.println("Security manager has been disabled ");
    }
    
    public void init() {
        System.err.println("Gonna set the security manager...");
        //~ System.out.println("toto");
        
        System.setSecurityManager(new SecurityManager()
        {
          @Override
          public void checkPermission(Permission permission) {
             if (permission instanceof CardPermission) {
                 return;
             }
             //~ if (permission instanceof RuntimePermission) {
                 //~ return;
             //~ }
             //~ if (permission instanceof FilePermission) {
                 //~ return;
             //~ }
             java.security.AccessController.checkPermission(permission);
          }
        });
        System.err.println("Initialized");
    }
    
    public String readCard() {
        
        try {
            TerminalFactory factory = TerminalFactory.getDefault();  
            List<CardTerminal> terminals = factory.terminals().list();          
            CardTerminal terminal = terminals.get(0);  
            
            if (! terminal.isCardPresent()){  
                return "No card found on terminal";
                //~ return new EidReaderResponse(new String[] { "No card found on terminal" });
            }
            
            Card card = terminal.connect("T=0");  
            //~ ATR atr = card.getATR();
            CardChannel channel = card.getBasicChannel();  

            //~ EstEID a = new EstEID();
            //~ a.init();
            PersonalFile pf = new PersonalFile(channel);
            //~ a.readCard();
            return pf.toString();
            //~ return new String[] { pf.toString() };
            //~ return new EidReaderResponse(pf.getData());
            //~ return pf.getSurName();
        } catch (Exception e) {
            //~ return new EidReaderResponse(new String[] { e.toString() });
            return e.toString();
        }
    }
}
