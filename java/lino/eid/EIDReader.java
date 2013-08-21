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
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;

import java.util.Arrays;  
import java.util.List; 

import java.awt.image.BufferedImage;

import javax.imageio.ImageIO;

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
    String s = "reader:EST\n";
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

class BelgianReader {
    public static final byte FIELD_COUNT = 16;
    private CardChannel cardChannel;
    String[] data = new String[FIELD_COUNT];
    public static final String[] fields = new String[] {
        "last_name","first_name", "other_names", "gender", "nationality",
        "birth_date","national_id","card_id","valid_until",
        "birth_place", "date_issued", "ResidencePermitType",
        "remark1",
        "remark2",
        "remark3",
        "remark4"
        };
    
	private static final int BLOCK_SIZE = 0xff;
    
	private final static byte[] ATR_PATTERN = new byte[] { 0x3b, (byte) 0x98,
			0x00, 0x40, 0x00, (byte) 0x00, 0x00, 0x00, 0x01, 0x01, (byte) 0xad,
			0x13, 0x10 };

	private final static byte[] ATR_MASK = new byte[] { (byte) 0xff,
			(byte) 0xff, 0x00, (byte) 0xff, 0x00, 0x00, 0x00, 0x00,
			(byte) 0xff, (byte) 0xff, (byte) 0xff, (byte) 0xff, (byte) 0xf0 };

	public static final byte[] IDENTITY_FILE_ID = new byte[] { 0x3F, 0x00,
			(byte) 0xDF, 0x01, 0x40, 0x31 };

	public static final byte[] ADDRESS_FILE_ID = new byte[] { 0x3F, 0x00,
			(byte) 0xDF, 0x01, 0x40, 0x33 };

	public static final byte[] PHOTO_FILE_ID = new byte[] { 0x3F, 0x00,
			(byte) 0xDF, 0x01, 0x40, 0x35 };

	public static boolean matchesEidAtr(ATR atr) { // from eid-applet-core...PcscEid.java
		byte[] atrBytes = atr.getBytes();
		if (atrBytes.length != ATR_PATTERN.length) {
			return false;
		}
		for (int idx = 0; idx < atrBytes.length; idx++) {
			atrBytes[idx] &= ATR_MASK[idx];
		}
		if (Arrays.equals(atrBytes, ATR_PATTERN)) {
			return true;
		}
		return false;
	}
    
    public BelgianReader(CardChannel channel) 
        throws CardException, IOException, UnsupportedEncodingException 
    {  
        this.cardChannel = channel;
        for (byte i = 0; i < FIELD_COUNT; i++) {  
            data[i] = "";
        }
        
        
        //~ byte[] photoFile = readFile(PHOTO_FILE_ID);
        //~ BufferedImage photo = ImageIO.read(new ByteArrayInputStream(photoFile));
        
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
        
		byte[] identityFile = readFile(IDENTITY_FILE_ID);
        System.err.println("identityFile.length is " + Integer.toString(identityFile.length));
        baos.write(identityFile);
        
        //~ baos.write('\n');
        
		byte[] addressFile = readFile(ADDRESS_FILE_ID);
        baos.write(addressFile);
        System.err.println("addressFile.length is " + Integer.toString(addressFile.length));
        
        //~ data[0] = baos.toString("utf-8");
        //~ data[0] = baos.toString("ISO-8859-1 ");
        data[0] = baos.toString();
    }  
    
	public byte[] readFile(byte[] fileId) throws CardException, IOException {
		selectFile(fileId);
		byte[] data = readBinary();
		return data;
	}
    
	private void selectFile(byte[] fileId) throws CardException,
			FileNotFoundException {
		CommandAPDU selectFileApdu = new CommandAPDU(0x00, 0xA4, 0x08, 0x0C,
				fileId);
		ResponseAPDU responseApdu = transmit(selectFileApdu);
		if (0x9000 != responseApdu.getSW()) {
			throw new FileNotFoundException(
					"wrong status word after selecting file: "
							+ Integer.toHexString(responseApdu.getSW()));
		}
		try {
			// SCARD_E_SHARING_VIOLATION fix
			Thread.sleep(20);
		} catch (InterruptedException e) {
			throw new RuntimeException("sleep error: " + e.getMessage());
		}
	}
    
	private byte[] readBinary() throws CardException, IOException {
		int offset = 0;
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		byte[] data;
		do {
			CommandAPDU readBinaryApdu = new CommandAPDU(0x00, 0xB0,
					offset >> 8, offset & 0xFF, BLOCK_SIZE);
			ResponseAPDU responseApdu = transmit(readBinaryApdu);
			int sw = responseApdu.getSW();
			if (0x6B00 == sw) {
				/*
				 * Wrong parameters (offset outside the EF) End of file reached.
				 * Can happen in case the file size is a multiple of 0xff bytes.
				 */
				break;
			}
			if (0x9000 != sw) {
				throw new IOException("APDU response error: "
						+ responseApdu.getSW());
			}

			/*
			 * Introduce some delay for old Belpic V1 eID cards.
			 */
			// try {
			// Thread.sleep(50);
			// } catch (InterruptedException e) {
			// throw new RuntimeException("sleep error: " + e.getMessage(), e);
			// }
			data = responseApdu.getData();
			baos.write(data);
			offset += data.length;
		} while (BLOCK_SIZE == data.length);
		return baos.toByteArray();
	}

    

    

	private ResponseAPDU transmit(CommandAPDU commandApdu) throws CardException {
		ResponseAPDU responseApdu = this.cardChannel.transmit(commandApdu);
		if (0x6c == responseApdu.getSW1()) {
			/*
			 * A minimum delay of 10 msec between the answer ‘6C xx’ and the
			 * next APDU is mandatory for eID v1.0 and v1.1 cards.
			 */
			try {
				Thread.sleep(10);
			} catch (InterruptedException e) {
				throw new RuntimeException("cannot sleep");
			}
			responseApdu = this.cardChannel.transmit(commandApdu);
		}
		return responseApdu;
	}

    
    
    @Override  
    public String toString() {  
      String s = "reader:BEL\n";
      for (byte i = 0; i < FIELD_COUNT; i++) {  
          s = s + fields[i] + ":" + data[i].trim() + "\n";
      }
      return s;
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
    
    public String readCard() 
        throws CardException, IOException 
    {
        
        //~ try {
            TerminalFactory factory = TerminalFactory.getDefault();  
            List<CardTerminal> terminals = factory.terminals().list();          
            CardTerminal terminal = terminals.get(0);  
            
            if (! terminal.isCardPresent()){  
                return "No card found on terminal";
                //~ return new EidReaderResponse(new String[] { "No card found on terminal" });
            }
            
            Card card = terminal.connect("T=0");  
            ATR atr = card.getATR();
            
            CardChannel channel = card.getBasicChannel();  
            
            if (BelgianReader.matchesEidAtr(atr)) {
                BelgianReader pf = new BelgianReader(channel);
                return pf.toString();
            }
            

            PersonalFile pf = new PersonalFile(channel);
            return pf.toString();
            //~ return new String[] { pf.toString() };
            //~ return new EidReaderResponse(pf.getData());
            //~ return pf.getSurName();
        //~ } catch (Exception e) {
            //~ return new EidReaderResponse(new String[] { e.toString() });
            //~ return e.toString();
        //~ }
    }
    
}
