

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

// to carry out validation of username and password from Login Table
//
public class Validation 
{

	public boolean validateLogin(String userName, String pwd)
	{ 
			
		try{
			
			if(userName.equalsIgnoreCase("kishan"))
			{	
					Class.forName("com.mysql.jdbc.Driver");  
					Connection con=DriverManager.getConnection("jdbc:mysql://192.168.43.224:3306/temps","monitor","password");  
					
					//update the status in Login Table
			        String abc1="insert into visitors values(?,curtime(),'checking')";
		            PreparedStatement ps3 = con.prepareStatement(abc1);
		            ps3.setString(1, userName);
		            //execution
		            ps3.executeUpdate();
		            con.close(); 
		
		            return true;
			}
			else
			{
					return false;
			}
		}

		catch (SQLException ex) 
		{ 
	   //error message
	   System.out.println ("\n*** SQLException caught ***\n" + ex.getMessage());
	   return false;
	    }
		catch (Exception e) 
		{
			System.out.println ("\n*** other Exception caught ***\n" +e.getMessage());	
			return false;
		}
}
}
