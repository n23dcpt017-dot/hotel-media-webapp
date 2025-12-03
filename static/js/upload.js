// ================================================
// FILE UPLOAD HANDLER
// ================================================

class FileUploader {
    constructor(dropzoneId, inputId, previewId) {
        this.dropzone = document.getElementById(dropzoneId);
        this.input = document.getElementById(inputId);
        this.preview = document.getElementById(previewId);
        this.files = [];
        
        this.init();
    }
    
    init() {
        if (!this.dropzone || !this.input) return;
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.dropzone.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });
        
        // Highlight dropzone when dragging
        ['dragenter', 'dragover'].forEach(eventName => {
            this.dropzone.addEventListener(eventName, () => {
                this.dropzone.classList.add('highlight');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            this.dropzone.addEventListener(eventName, () => {
                this.dropzone.classList.remove('highlight');
            }, false);
        });
        
        // Handle drop
        this.dropzone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        }, false);
        
        // Handle click to browse
        this.dropzone.addEventListener('click', () => {
            this.input.click();
        });
        
        // Handle file input change
        this.input.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }
    
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    handleFiles(files) {
        Array.from(files).forEach(file => {
            // Validate file
            if (this.validateFile(file)) {
                this.files.push(file);
                this.previewFile(file);
            }
        });
    }
    
    validateFile(file) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedTypes = [
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/webp',
            'video/mp4',
            'video/avi',
            'video/mov'
        ];
        
        if (file.size > maxSize) {
            alert(`File "${file.name}" quá lớn! Kích thước tối đa: 16MB`);
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            alert(`File "${file.name}" không được hỗ trợ!`);
            return false;
        }
        
        return true;
    }
    
    previewFile(file) {
        if (!this.preview) return;
        
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const item = document.createElement('div');
            item.className = 'file-preview-item';
            
            let content = '';
            
            if (file.type.startsWith('image/')) {
                content = `
                    <img src="${e.target.result}" alt="${file.name}" class="file-preview-image">
                `;
            } else if (file.type.startsWith('video/')) {
                content = `
                    <video src="${e.target.result}" class="file-preview-video" controls></video>
                `;
            }
            
            item.innerHTML = `
                ${content}
                <div class="file-preview-info">
                    <div class="file-preview-name" title="${file.name}">${file.name}</div>
                    <div class="file-preview-size">${this.formatFileSize(file.size)}</div>
                    <div class="file-preview-actions">
                        <button class="file-delete-btn" onclick="removeFile('${file.name}')">
                            <i class="fas fa-trash"></i> Xóa
                        </button>
                    </div>
                </div>
            `;
            
            this.preview.appendChild(item);
        };
        
        reader.readAsDataURL(file);
    }
    
    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }
    
    async uploadFiles() {
        if (this.files.length === 0) {
            alert('Vui lòng chọn file để upload!');
            return;
        }
        
        const formData = new FormData();
        this.files.forEach((file, index) => {
            formData.append('files[]', file);
        });
        
        try {
            // Show progress
            const progressDiv = document.createElement('div');
            progressDiv.className = 'upload-progress';
            progressDiv.innerHTML = `
                <div class="progress-text">Đang upload...</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
            `;
            this.dropzone.after(progressDiv);
            
            const response = await fetch('/media/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            progressDiv.remove();
            
            if (result.success) {
                alert('Upload thành công!');
                window.location.reload();
            } else {
                alert('Upload thất bại: ' + result.error);
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('Đã xảy ra lỗi khi upload!');
        }
    }
}

// Remove file from preview
function removeFile(filename) {
    if (!confirm(`Xóa file "${filename}"?`)) return;
    
    // Remove from preview
    const items = document.querySelectorAll('.file-preview-item');
    items.forEach(item => {
        const name = item.querySelector('.file-preview-name');
        if (name && name.textContent === filename) {
            item.remove();
        }
    });
}

// Initialize uploader
let uploader;
document.addEventListener('DOMContentLoaded', function() {
    uploader = new FileUploader('upload-dropzone', 'file-input', 'file-preview');
});

// Submit upload
function submitUpload() {
    if (uploader) {
        uploader.uploadFiles();
    }
}
