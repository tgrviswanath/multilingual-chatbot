"""
FAQ intent dataset and response templates.
Intents cover common customer support + general FAQ scenarios.
"""

INTENTS = {
    "greeting": {
        "examples": [
            "hello", "hi", "hey", "good morning", "good afternoon",
            "good evening", "howdy", "what's up", "greetings",
        ],
        "response": "Hello! How can I help you today?",
    },
    "farewell": {
        "examples": [
            "bye", "goodbye", "see you", "take care", "later",
            "have a good day", "talk to you later", "cya",
        ],
        "response": "Goodbye! Have a great day. Feel free to come back anytime!",
    },
    "hours": {
        "examples": [
            "what are your hours", "when are you open", "opening hours",
            "business hours", "what time do you close", "are you open on weekends",
            "working hours", "office hours",
        ],
        "response": "We are open Monday to Friday, 9 AM to 6 PM (EST). On weekends we offer limited support via email.",
    },
    "pricing": {
        "examples": [
            "how much does it cost", "what is the price", "pricing plans",
            "how much is the subscription", "cost of the service",
            "what are your rates", "is there a free plan", "pricing information",
        ],
        "response": "We offer three plans: Basic ($9/month), Pro ($29/month), and Enterprise (custom pricing). Visit our pricing page for full details.",
    },
    "refund": {
        "examples": [
            "I want a refund", "how do I get my money back", "refund policy",
            "cancel my subscription", "request a refund", "money back guarantee",
            "return policy", "can I get a refund",
        ],
        "response": "We offer a 30-day money-back guarantee. To request a refund, please contact support@example.com with your order ID.",
    },
    "contact": {
        "examples": [
            "how do I contact you", "support email", "phone number",
            "how to reach you", "customer service contact", "get in touch",
            "talk to a human", "speak to an agent",
        ],
        "response": "You can reach us at support@example.com or call +1-800-555-0100. Live chat is available on our website during business hours.",
    },
    "account": {
        "examples": [
            "how do I reset my password", "forgot my password", "change email",
            "update my account", "delete my account", "login problem",
            "can't log in", "account settings",
        ],
        "response": "For account issues, visit the Account Settings page or click 'Forgot Password' on the login screen. Need more help? Contact support.",
    },
    "shipping": {
        "examples": [
            "how long does shipping take", "track my order", "delivery time",
            "where is my package", "shipping options", "express delivery",
            "international shipping", "order status",
        ],
        "response": "Standard shipping takes 3-5 business days. Express shipping (1-2 days) is available at checkout. Track your order using the link in your confirmation email.",
    },
    "thanks": {
        "examples": [
            "thank you", "thanks", "thank you so much", "appreciate it",
            "that was helpful", "great help", "cheers",
        ],
        "response": "You're welcome! Is there anything else I can help you with?",
    },
    "unknown": {
        "examples": [],
        "response": "I'm sorry, I didn't quite understand that. Could you rephrase your question? You can also contact our support team at support@example.com.",
    },
}
