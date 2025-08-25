/**
 * Video Upload Progress Handler
 * Handles chunked file uploads with real-time progress tracking
 */

class VideoUploader {
    constructor(options) {
        this.fileInput = options.fileInput;
        this.progressContainer = options.progressContainer;
        this.progressBar = options.progressBar;
        this.progressText = options.progressText;
        this.form = options.form;
        this.submitButton = options.submitButton;
        
        this.chunkSize = 1024 * 1024; // 1MB chunks
        this.uploadId = null;
        this.currentFile = null;
        this.isUploading = false;
        
        this.init();
    }
    
    init() {
        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
        
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        // Validate file type
        const allowedTypes = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska'];
        if (!allowedTypes.includes(file.type)) {
            this.showError('Please select a valid video file (MP4, WebM, OGG, MOV, AVI, MKV)');
            return;
        }
        
        // Validate file size (max 500MB)
        const maxSize = 500 * 1024 * 1024;
        if (file.size > maxSize) {
            this.showError('File size must be less than 500MB');
            return;
        }
        
        this.currentFile = file;
        this.uploadId = this.generateUploadId();
        
        // Show file info
        this.showFileInfo(file);
    }
    
    handleFormSubmit(event) {
        event.preventDefault();
        
        if (!this.currentFile) {
            this.showError('Please select a video file');
            return;
        }
        
        if (this.isUploading) {
            return;
        }
        
        this.startUpload();
    }
    
    async startUpload() {
        this.isUploading = true;
        this.showProgress();
        this.disableForm();
        
        try {
            const totalChunks = Math.ceil(this.currentFile.size / this.chunkSize);
            
            // Upload chunks
            for (let chunkNumber = 0; chunkNumber < totalChunks; chunkNumber++) {
                const start = chunkNumber * this.chunkSize;
                const end = Math.min(start + this.chunkSize, this.currentFile.size);
                const chunk = this.currentFile.slice(start, end);
                
                const response = await this.uploadChunk(chunk, chunkNumber, totalChunks);
                
                if (response.status === 'complete') {
                    // Upload completed, now create the lecture
                    await this.createLecture(response.filename);
                    return;
                }
                
                // Update progress
                this.updateProgress(response.progress, response.message);
            }
        } catch (error) {
            this.showError('Upload failed: ' + error.message);
            this.enableForm();
        }
        
        this.isUploading = false;
    }
    
    async uploadChunk(chunk, chunkNumber, totalChunks) {
        const formData = new FormData();
        formData.append('chunk', chunk);
        formData.append('upload_id', this.uploadId);
        formData.append('chunk_number', chunkNumber);
        formData.append('total_chunks', totalChunks);
        formData.append('filename', this.currentFile.name);
        
        const response = await fetch('/instructor/lectures/upload_progress', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': this.getCSRFToken()
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        return await response.json();
    }
    
    async createLecture(videoFilename) {
        const formData = new FormData();
        
        // Get form data
        const titleInput = this.form.querySelector('[name="title"]');
        const descriptionInput = this.form.querySelector('[name="description"]');
        const courseIdInput = this.form.querySelector('[name="course_id"]');
        const thumbnailInput = this.form.querySelector('[name="thumbnail"]');
        const isPublishedInput = this.form.querySelector('[name="is_published"]');
        
        formData.append('title', titleInput.value);
        formData.append('description', descriptionInput.value);
        formData.append('course_id', courseIdInput.value);
        formData.append('is_published', isPublishedInput.checked);
        formData.append('video_filename', videoFilename);
        
        if (thumbnailInput.files[0]) {
            formData.append('thumbnail', thumbnailInput.files[0]);
        }
        
        const response = await fetch('/instructor/lectures/create_with_upload', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': this.getCSRFToken()
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            this.showSuccess(result.message);
            setTimeout(() => {
                window.location.href = result.redirect_url;
            }, 2000);
        } else {
            throw new Error(result.error || 'Failed to create lecture');
        }
    }
    
    showProgress() {
        if (this.progressContainer) {
            this.progressContainer.style.display = 'block';
        }
    }
    
    updateProgress(percentage, message) {
        if (this.progressBar) {
            this.progressBar.style.width = percentage + '%';
            this.progressBar.setAttribute('aria-valuenow', percentage);
        }
        
        if (this.progressText) {
            this.progressText.textContent = message || `${Math.round(percentage)}% uploaded`;
        }
    }
    
    showFileInfo(file) {
        const fileSize = this.formatFileSize(file.size);
        const fileInfo = document.getElementById('file-info');
        if (fileInfo) {
            fileInfo.innerHTML = `
                <div class="alert alert-info">
                    <strong>Selected file:</strong> ${file.name}<br>
                    <strong>Size:</strong> ${fileSize}<br>
                    <strong>Type:</strong> ${file.type}
                </div>
            `;
        }
    }
    
    showError(message) {
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            alertContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }
    
    showSuccess(message) {
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            alertContainer.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }
    
    disableForm() {
        if (this.submitButton) {
            this.submitButton.disabled = true;
            this.submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        }
        
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => input.disabled = true);
    }
    
    enableForm() {
        if (this.submitButton) {
            this.submitButton.disabled = false;
            this.submitButton.innerHTML = 'Upload Lecture';
        }
        
        const inputs = this.form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => input.disabled = false);
    }
    
    generateUploadId() {
        return 'upload_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    getCSRFToken() {
        const token = document.querySelector('meta[name=csrf-token]');
        return token ? token.getAttribute('content') : '';
    }
}

// Initialize uploader when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('lecture-upload-form');
    if (uploadForm) {
        new VideoUploader({
            fileInput: document.getElementById('video'),
            progressContainer: document.getElementById('upload-progress'),
            progressBar: document.getElementById('progress-bar'),
            progressText: document.getElementById('progress-text'),
            form: uploadForm,
            submitButton: document.getElementById('submit-button')
        });
    }
});