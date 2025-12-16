// components/DocumentUpload.jsx
// React component for uploading documents to the RAG backend
import React, { useState } from 'react';
import ragApiClient from '../api/rag-api';

const DocumentUpload = ({ onUploadSuccess }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [progress, setProgress] = useState(0);
  const [documentInfo, setDocumentInfo] = useState({
    title: '',
    author: '',
    sourceType: 'book',
    content: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setDocumentInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadStatus('Uploading file...');
    setIsUploading(true);
    setProgress(0);

    try {
      // Simulate progress (in a real implementation, you'd track actual upload progress)
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(interval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const result = await ragApiClient.uploadDocumentFile(file, {
        title: documentInfo.title || file.name,
        author: documentInfo.author,
        sourceType: documentInfo.sourceType
      });

      clearInterval(interval);
      setProgress(100);
      setUploadStatus('Document uploaded and indexed successfully!');

      if (onUploadSuccess) {
        onUploadSuccess(result);
      }

      // Reset form after successful upload
      setDocumentInfo({
        title: '',
        author: '',
        sourceType: 'book',
        content: ''
      });
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus(`Upload failed: ${error.message}`);
    } finally {
      setIsUploading(false);
      setTimeout(() => setUploadStatus(''), 5000); // Clear status after 5 seconds
    }
  };

  const handleTextUpload = async (e) => {
    e.preventDefault();
    if (!documentInfo.content.trim()) return;

    setIsUploading(true);
    setUploadStatus('Processing document...');

    try {
      const result = await ragApiClient.uploadDocument(
        documentInfo.title || 'Untitled Document',
        documentInfo.content,
        {
          author: documentInfo.author,
          sourceType: documentInfo.sourceType
        }
      );

      setUploadStatus('Document uploaded and indexed successfully!');

      if (onUploadSuccess) {
        onUploadSuccess(result);
      }

      // Reset form after successful upload
      setDocumentInfo({
        title: '',
        author: '',
        sourceType: 'book',
        content: ''
      });
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus(`Upload failed: ${error.message}`);
    } finally {
      setIsUploading(false);
      setTimeout(() => setUploadStatus(''), 5000); // Clear status after 5 seconds
    }
  };

  return (
    <div className="document-upload-container">
      <h3>Upload Document for RAG</h3>

      {uploadStatus && (
        <div className={`upload-status ${uploadStatus.includes('failed') ? 'error' : 'success'}`}>
          {uploadStatus}
          {progress > 0 && progress < 100 && (
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleTextUpload} className="text-upload-form">
        <div className="form-group">
          <label htmlFor="title">Document Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={documentInfo.title}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="author">Author</label>
          <input
            type="text"
            id="author"
            name="author"
            value={documentInfo.author}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="sourceType">Source Type</label>
          <select
            id="sourceType"
            name="sourceType"
            value={documentInfo.sourceType}
            onChange={handleInputChange}
          >
            <option value="book">Book</option>
            <option value="article">Article</option>
            <option value="chapter">Chapter</option>
            <option value="section">Section</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="content">Document Content</label>
          <textarea
            id="content"
            name="content"
            value={documentInfo.content}
            onChange={handleInputChange}
            placeholder="Paste your document content here, or upload a file below"
            rows="10"
          />
        </div>

        <button
          type="submit"
          disabled={isUploading || !documentInfo.content.trim()}
        >
          {isUploading ? 'Uploading...' : 'Upload Text'}
        </button>
      </form>

      <div className="divider">OR</div>

      <div className="file-upload-section">
        <label htmlFor="file-upload" className="file-upload-label">
          Upload Document File
        </label>
        <input
          type="file"
          id="file-upload"
          accept=".txt,.pdf,.doc,.docx,.md" // Adjust accepted file types as needed
          onChange={handleFileUpload}
          disabled={isUploading}
          style={{ display: 'none' }}
        />
        <p>Supported formats: TXT, PDF, DOC, DOCX, MD</p>
      </div>

      <div className="upload-notes">
        <h4>Notes:</h4>
        <ul>
          <li>Documents are processed and indexed in the RAG system</li>
          <li>After upload, the document will be available for Q&A</li>
          <li>Large documents may take a few minutes to process</li>
        </ul>
      </div>
    </div>
  );
};

export default DocumentUpload;