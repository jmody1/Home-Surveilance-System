

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/WelcomeServlet")
public class WelcomeServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    
    public WelcomeServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		HttpSession session=request.getSession();
		try{
			
			System.out.println("WelcomeServlet.doPost()");
			
			
			//to view log details
			if (request.getParameter("logs") != null) 
			{
				RequestDispatcher rs= request.getRequestDispatcher("Visitors.jsp");
				rs.forward(request, response);
	        } 
			
		}// to handle exceptions
		catch (Exception e){System.out.println("Technical Error");}
		
	}

}
