# TMF621 Trouble Ticket API - Workshop Edition

A fully functional implementation of TM Forum's TMF621 Trouble Ticket Management API for training and workshops.

## 🚀 Quick Deploy to Railway

### Prerequisites
- GitHub account
- Railway account (free tier works great)

### Deployment Steps (Keyboard Navigation)

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "TMF621 API implementation"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Navigate to [railway.app](https://railway.app)
   - Tab to "Login" and press Enter
   - After login, Tab to "New Project" and press Enter
   - Select "Deploy from GitHub repo" using arrow keys and Enter
   - Choose your repository
   - Railway will auto-detect Python and deploy!

3. **Get Your API URL:**
   - Navigate to Settings tab (use Tab/Shift+Tab)
   - Find "Generate Domain" button and press Enter
   - Your API will be available at: `https://your-app.railway.app`

## 📚 Workshop Usage

### API Endpoints

**Base URL:** `https://your-app.railway.app/tmf-api/troubleTicket/v5`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/troubleTicket` | List all tickets (with filters) |
| POST | `/troubleTicket` | Create new ticket |
| GET | `/troubleTicket/{id}` | Get specific ticket |
| PATCH | `/troubleTicket/{id}` | Update ticket |
| DELETE | `/troubleTicket/{id}` | Delete ticket |

### Sample Data

The API comes pre-loaded with 10 delightfully silly trouble tickets for workshop fun:
- Critical kitchen emergencies (toast stuck in toaster, smoke alarms)
- Slapstick mishaps (spaghetti on ceiling, flour explosions)
- Culinary complaints (salt-sugar mix-ups, frozen pizza fails)
- Pet-related incidents (cake-eating dogs with sugar zoomies)
- Success stories (3 days of successful toast-making!)

The humorous data makes workshops more engaging while demonstrating real API patterns!

### Testing with Postman

#### Create a New Ticket
```http
POST /tmf-api/troubleTicket/v5/troubleTicket
Content-Type: application/json

{
  "description": "Blender lid forgotten. Kitchen ceiling now decorated with smoothie art.",
  "severity": "major",
  "priority": 2,
  "type": "trouble",
  "channel": "phone"
}
```

#### List All Tickets
```http
GET /tmf-api/troubleTicket/v5/troubleTicket
```

#### Filter by Severity
```http
GET /tmf-api/troubleTicket/v5/troubleTicket?severity=critical
```

#### Filter by Status
```http
GET /tmf-api/troubleTicket/v5/troubleTicket?status=inProgress
```

#### Update Ticket Status
```http
PATCH /tmf-api/troubleTicket/v5/troubleTicket/{id}
Content-Type: application/json

{
  "status": "resolved",
  "resolutionDate": "2026-01-07T15:30:00Z"
}
```

## 🎯 Workshop Exercises

### Exercise 1: Basic CRUD
1. List all tickets
2. Create a new trouble ticket for "Oven timer went off. No one home. Neighbors concerned."
3. Retrieve the created ticket by ID
4. Update the ticket status to "inProgress"
5. Mark it as "resolved"

### Exercise 2: Filtering & Search
1. Find all critical severity tickets (the really dramatic kitchen fails!)
2. Find all tickets in "acknowledged" status
3. Combine filters (if needed)

### Exercise 3: Workflow Simulation
1. Create a new incident ticket: "Cat walked across keyboard. Ordered 47 pizzas."
2. Update priority based on pizza count
3. Add expected resolution date
4. Mark as resolved when pizzas are cancelled

### Exercise 4: API Design Analysis
- Examine the response structure
- Note the use of href for resource links
- Understand RESTful patterns in TMF APIs
- Enjoy the creative descriptions!

## 📋 Field Reference

### Ticket Severities
- `critical` - Service affecting, immediate action required
- `major` - Significant impact, urgent attention needed
- `minor` - Low impact, can be scheduled

### Ticket Statuses
- `acknowledged` - Ticket received and assigned
- `pending` - Waiting for information/resources
- `inProgress` - Actively being worked on
- `resolved` - Issue fixed, awaiting closure
- `closed` - Fully complete

### Ticket Types
- `incident` - Unplanned service interruption
- `trouble` - Service degradation
- `request` - Feature/change request
- `complaint` - Customer complaint
- `feedback` - General feedback

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python main.py

# API available at: http://localhost:8000

# Seed sample data
python seed_data.py
```

## 📖 API Documentation

Once deployed, access the beautiful Scalar API documentation:
- **Scalar UI**: `https://your-app.railway.app/docs`

Scalar provides a modern, interactive API reference with:
- Clean, readable interface
- Try-it-out functionality for all endpoints
- Request/response examples
- Full keyboard navigation support

## 🎓 Learning Resources

- [TM Forum TMF621 Specification](https://www.tmforum.org/resources/specification/tmf621-trouble-ticket-api-rest-specification-r19-5-0/)
- [OpenAPI 3.0 Guide](https://swagger.io/specification/)
- [RESTful API Best Practices](https://restfulapi.net/)

## 💡 Workshop Tips

**For Non-Technical Participants:**
- Focus on understanding the API structure
- Use Postman collections to explore without coding
- Try the exercises in sequence

**For Developers:**
- Examine the OpenAPI specification
- Consider how this integrates with other TMF APIs
- Think about error handling and validation

**For Workshop Leaders:**
- Share the Railway URL before the session
- Import the Postman collection into a workspace
- Have participants test creating tickets with their names

## 🐛 Troubleshooting

**API not responding:**
- Check Railway deployment logs (Settings > Deployments tab)
- Verify the domain was generated

**No data showing:**
- The seed script runs automatically on deployment
- Check `/health` endpoint: `https://your-app.railway.app/health`

**Can't create tickets:**
- Verify Content-Type header is `application/json`
- Check the request body matches the schema

## 📞 Support

For issues or questions during the workshop, check:
1. API health endpoint: `/health`
2. Interactive docs: `/docs`
3. Railway logs in the dashboard

---

**Built with FastAPI, SQLAlchemy, and ❤️ for TM Forum API training**
