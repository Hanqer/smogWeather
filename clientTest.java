import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import net.sf.json.JSONArray;

class Conn implements Runnable
{
	public void run()
	{
		String qer = "10.190.84.150";
		try
        {
            Socket socket = new Socket("localhost", 8888);
            PrintWriter out = new PrintWriter(socket.getOutputStream());
            BufferedReader in = new BufferedReader(new InputStreamReader(
            socket.getInputStream()));
            out.println("sdsdddvvvvvvvvvvvvvvvvvvads");
            out.flush();
            String tmp = null;
            String info = "";
            while((tmp = in.readLine())!= null)
            info += tmp;
            System.out.println(info);
            socket.close();
        }
        catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
}
public class Test {

    public static void main(String[] args) {
      
        	 new  Thread(new Conn()).start();
        	 new  Thread(new Conn()).start();
        	new  Thread(new Conn()).start();
        	 new  Thread(new Conn()).start();
        	 new  Thread(new Conn()).start();
        	 
        
    }
}
