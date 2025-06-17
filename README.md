# Middleware Integration System

## Description
This project is a middleware system that integrates Mattermost with ERPNext. It processes messages from Mattermost, analyzes them using an AI engine, and performs actions in ERPNext based on the detected intent.

## Architecture
The system follows a modular architecture with clear separation of concerns:

## Processing Flow
1. User sends a message in Mattermost
2. Mattermost sends a webhook to the middleware
3. The middleware parses the webhook data
4. The message text is sent to the AI engine for analysis
5. Based on the detected intent, appropriate actions are performed in ERPNext
6. The result is formatted and sent back to Mattermost

## Installation

### Requirements
- Python 3.8 or higher
- Mattermost server
- ERPNext server
- Internet connection for AI services

### Installing Libraries
```bash
pip install -r requirements.txt
```

### Configuration
Copy the example environment file and configure it with your settings:
```bash
cp .env
```

Edit the `.env` file to set your Mattermost and ERPNext credentials, as well as other configuration options.

## Running the Application

### Direct Execution
```bash
python main.py

## API Endpoints

### Mattermost Webhook
- **URL**: `/webhook/mattermost`
- **Method**: POST
- **Description**: Receives webhooks from Mattermost

## Testing

Run the tests using pytest:
```bash
pytest
```

Or run specific test files:
```bash
pytest test/test_mattermost_handler.py
pytest test/test_erp_handler.py
pytest test/test_full_flow.py
```

## Project Structure
```
├── main.py                 # Application entry point
├── handlers/                  # API route handlers
│   └── mattermost_handler.py
├── services/               # Core services
│   ├── ai_service.py        # AI analysis service
│   ├── erp_service.py      # ERPNext integration
│   └── mattermost_service.py # Mattermost integration
├── test/                   # Test files
│   ├── test_mattermost_handler.py
│   ├── test_erp_handler.py
│   └── test_full_flow.py
├── logs/                   # Log files
├── .env.example           # Example environment variables
├── requirements.txt        # Python dependencies
└── run.sh                  # Startup script
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.