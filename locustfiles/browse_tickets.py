from locust import HttpUser,task,between
from random import randint

class UserTickets(HttpUser):
    wait_time = between(1,5)

    @task(2)
    def view_tickets(self):
        self.client.get('/tickets/', name='Ticket_management/tickets')

    @task(3)
    def view_ticketdetails(self):
        ticket_id = randint(1,10)
        self.client.get(f'/tickets/{ticket_id}/', name="Ticket_management/tickets/:id")
    
    @task(8)
    def create_ticket(self):
        user_id = randint(1,10)
        self.client.post('/tickets/')
        json={
            "title":"Test title",
            "location":"Nairobi",
            "description":"Test issue",
            "status":"P",
            "user":user_id
        }

