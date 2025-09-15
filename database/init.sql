-- Database initialization script for Personalized Educational Assistant

-- Create database (run this separately if needed)
-- CREATE DATABASE educational_assistant;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles table (learning preferences and history)
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    learning_style VARCHAR(50), -- visual, auditory, kinesthetic, reading
    difficulty_level VARCHAR(20) DEFAULT 'beginner', -- beginner, intermediate, advanced
    subjects_of_interest TEXT[], -- array of subjects
    preferred_explanation_length VARCHAR(20) DEFAULT 'medium', -- short, medium, detailed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learning sessions table
CREATE TABLE learning_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(200) NOT NULL,
    session_type VARCHAR(50) NOT NULL, -- explanation, quiz, evaluation
    content TEXT NOT NULL,
    user_input TEXT,
    ai_response TEXT,
    session_data JSONB, -- flexible data storage for different session types
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quiz questions and answers
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES learning_sessions(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    options JSONB NOT NULL, -- array of answer options
    correct_answer INTEGER NOT NULL, -- index of correct option
    explanation TEXT,
    difficulty_level VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User quiz responses
CREATE TABLE quiz_responses (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES quiz_questions(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    selected_answer INTEGER NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_taken INTEGER, -- seconds
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learning progress tracking
CREATE TABLE learning_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic VARCHAR(200) NOT NULL,
    mastery_level DECIMAL(3,2) DEFAULT 0.0, -- 0.0 to 1.0
    total_sessions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    last_studied TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX idx_learning_sessions_created_at ON learning_sessions(created_at);
CREATE INDEX idx_quiz_questions_session_id ON quiz_questions(session_id);
CREATE INDEX idx_quiz_responses_user_id ON quiz_responses(user_id);
CREATE INDEX idx_learning_progress_user_id ON learning_progress(user_id);
CREATE INDEX idx_learning_progress_topic ON learning_progress(topic); 
