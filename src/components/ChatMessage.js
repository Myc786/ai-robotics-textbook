import React from 'react';
import styles from './ChatMessage.module.css';

const ChatMessage = ({ message }) => {
  const { text, sender, sources } = message;

  return (
    <div className={`${styles.message} ${styles[sender]}`}>
      <div className={styles.messageText}>{text}</div>
      {sources && sources.length > 0 && (
        <div className={styles.sources}>
          <strong>Sources:</strong>
          <ul>
            {sources.map((source, index) => (
              <li key={index}>
                <a
                  href={source}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                >
                  {source.replace(/^https?:\/\//, '').substring(0, 50)}...
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;