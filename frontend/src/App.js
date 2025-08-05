import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Configure axios to use the backend URL
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'http://localhost:8000' 
  : 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showLoanForm, setShowLoanForm] = useState(false);
  const [loanFormData, setLoanFormData] = useState({
    name: '',
    income: '',
    family_size: 1,
    loan_balance: '',
    loan_type: 'federal',
    current_plan: 'standard'
  });
  const [isCalculating, setIsCalculating] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: inputMessage,
        history: messages
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        tools_used: response.data.tools_used,
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoanCalculator = async () => {
    if (!loanFormData.name || !loanFormData.income || !loanFormData.loan_balance) {
      alert('Please fill in all required fields (Name, Income, and Loan Balance)');
      return;
    }

    setIsCalculating(true);
    setShowLoanForm(false);

    try {
      const response = await axios.post(`${API_BASE_URL}/loan-calculator`, {
        name: loanFormData.name,
        income: parseFloat(loanFormData.income),
        family_size: parseInt(loanFormData.family_size),
        loan_balance: parseFloat(loanFormData.loan_balance),
        loan_type: loanFormData.loan_type,
        current_plan: loanFormData.current_plan
      });

      const timelineMessage = {
        role: 'assistant',
        content: response.data.timeline,
        tools_used: ['complete_form_tool', 'timeline_tool'],
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, timelineMessage]);
    } catch (error) {
      console.error('Error calculating loan:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error while calculating your loan timeline. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsCalculating(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLoanFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 Student Loan AI Assistant</h1>
        <p>Ask me anything about student loans, repayment plans, and the new RAP plan!</p>
        <button 
          className="loan-calculator-btn"
          onClick={() => setShowLoanForm(true)}
        >
          💰 Loan Calculator
        </button>
      </header>

      {/* Loan Calculator Modal */}
      {showLoanForm && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Loan Calculator</h2>
              <button 
                className="close-btn"
                onClick={() => setShowLoanForm(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label htmlFor="name">Full Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={loanFormData.name}
                  onChange={handleInputChange}
                  placeholder="Enter your full name"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="income">Annual Income *</label>
                <input
                  type="number"
                  id="income"
                  name="income"
                  value={loanFormData.income}
                  onChange={handleInputChange}
                  placeholder="Enter your annual income"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="family_size">Family Size</label>
                <select
                  id="family_size"
                  name="family_size"
                  value={loanFormData.family_size}
                  onChange={handleInputChange}
                >
                  <option value={1}>1 person</option>
                  <option value={2}>2 people</option>
                  <option value={3}>3 people</option>
                  <option value={4}>4 people</option>
                  <option value={5}>5+ people</option>
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="loan_balance">Total Loan Balance *</label>
                <input
                  type="number"
                  id="loan_balance"
                  name="loan_balance"
                  value={loanFormData.loan_balance}
                  onChange={handleInputChange}
                  placeholder="Enter your total loan balance"
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="loan_type">Loan Type</label>
                <select
                  id="loan_type"
                  name="loan_type"
                  value={loanFormData.loan_type}
                  onChange={handleInputChange}
                >
                  <option value="federal">Federal</option>
                  <option value="private">Private</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>
              
              <div className="form-group">
                <label htmlFor="current_plan">Current Repayment Plan</label>
                <select
                  id="current_plan"
                  name="current_plan"
                  value={loanFormData.current_plan}
                  onChange={handleInputChange}
                >
                  <option value="standard">Standard</option>
                  <option value="save">SAVE</option>
                  <option value="paye">PAYE</option>
                  <option value="ibr">IBR</option>
                  <option value="icr">ICR</option>
                </select>
              </div>
            </div>
            <div className="modal-footer">
              <button 
                className="cancel-btn"
                onClick={() => setShowLoanForm(false)}
              >
                Cancel
              </button>
              <button 
                className="generate-btn"
                onClick={handleLoanCalculator}
                disabled={isCalculating}
              >
                {isCalculating ? 'Generating...' : 'Generate Timeline'}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="chat-container">
        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h3>Welcome to the Student Loan AI Assistant!</h3>
              <p>I can help you with:</p>
              <ul>
                <li>Understanding the new RAP (Repayment Assistance Plan)</li>
                <li>Comparing different repayment plans (SAVE, PAYE, IBR)</li>
                <li>Loan timeline simulations</li>
                <li>Latest news and updates about student loans</li>
              </ul>
              <p>Try asking me something like: "What is the new RAP plan?" or "How does SAVE compare to the new plan?"</p>
              <p>Or click the "Loan Calculator" button above to get a personalized timeline!</p>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                <div className="message-text">{message.content}</div>
                {message.tools_used && message.tools_used.length > 0 && (
                  <div className="tools-used">
                    <small>Tools used: {message.tools_used.join(', ')}</small>
                  </div>
                )}
                <div className="message-timestamp">{message.timestamp}</div>
              </div>
            </div>
          ))}

          {(isLoading || isCalculating) && (
            <div className="message assistant">
              <div className="message-content">
                <div className="loading-indicator">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <div className="loading-text">
                    {isCalculating ? 'Generating your personalized timeline...' : 'Thinking...'}
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about student loans..."
              disabled={isLoading || isCalculating}
              rows="1"
            />
            <button 
              onClick={sendMessage} 
              disabled={isLoading || isCalculating || !inputMessage.trim()}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 