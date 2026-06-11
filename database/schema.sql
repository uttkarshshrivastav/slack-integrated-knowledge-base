-- Create messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message_id VARCHAR(255) UNIQUE NOT NULL,
    author VARCHAR(255) NOT NULL,
    channel VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    thread_id VARCHAR(255),
    message_text TEXT NOT NULL
);

-- Create resources table
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    url VARCHAR(2048) UNIQUE NOT NULL,
    title VARCHAR(255),
    content TEXT,
    summary TEXT,
    scrape_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create resource_mentions table
CREATE TABLE resource_mentions (
    id SERIAL PRIMARY KEY,
    message_id VARCHAR(255) NOT NULL,
    resource_id INTEGER NOT NULL,
    FOREIGN KEY (message_id) REFERENCES messages(message_id),
    FOREIGN KEY (resource_id) REFERENCES resources(id),
    UNIQUE (message_id, resource_id)
);
