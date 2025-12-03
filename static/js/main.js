// ================================================
// HOTEL MEDIA WEBAPP - MAIN JAVASCRIPT
// ================================================

// === MODAL FUNCTIONS ===
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}

// === CONFIRM DELETE ===
function confirmDelete(itemName) {
    return confirm(`Bạn có chắc muốn xóa "${itemName}" không? Hành động này không thể hoàn tác.`);
}

// === FLASH MESSAGES AUTO HIDE ===
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// === FORM VALIDATION ===
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            input.style.borderColor = 'var(--border)';
        }
    });
    
    if (!isValid) {
        alert('Vui lòng điền đầy đủ các trường bắt buộc!');
    }
    
    return isValid;
}

// === FILE UPLOAD PREVIEW ===
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

// === SEARCH FILTER ===
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const text = row.textContent.toLowerCase();
            
            if (text.includes(filter)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// === COPY TO CLIPBOARD ===
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Đã copy vào clipboard!');
    });
}

// === TOGGLE SIDEBAR (Mobile) ===
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

// === CHARACTER COUNTER ===
function characterCounter(textareaId, counterId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    
    if (!textarea || !counter) return;
    
    textarea.addEventListener('input', function() {
        const length = this.value.length;
        counter.textContent = `${length}/${maxLength}`;
        
        if (length > maxLength) {
            counter.style.color = 'var(--danger-color)';
        } else {
            counter.style.color = 'var(--text-secondary)';
        }
    });
}

// === AJAX REQUEST HELPER ===
async function fetchData(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi. Vui lòng thử lại!');
        return null;
    }
}

// === APPROVE/REJECT COMMENTS ===
async function approveComment(commentId) {
    if (!confirm('Duyệt bình luận này?')) return;
    
    const result = await fetchData(`/binhluan/duyet/${commentId}`, 'POST');
    if (result && result.success) {
        alert('Đã duyệt bình luận!');
        location.reload();
    }
}

async function rejectComment(commentId) {
    if (!confirm('Từ chối bình luận này?')) return;
    
    const result = await fetchData(`/binhluan/tu-choi/${commentId}`, 'POST');
    if (result && result.success) {
        alert('Đã từ chối bình luận!');
        location.reload();
    }
}

// === PUBLISH POST ===
async function publishPost(postId) {
    if (!confirm('Xuất bản bài viết này?')) return;
    
    const result = await fetchData(`/baiviet/xuat-ban/${postId}`, 'POST');
    if (result && result.success) {
        alert('Đã xuất bản bài viết!');
        location.reload();
    }
}

// === ACTIVE MENU HIGHLIGHT ===
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu a');
    
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// === TOOLTIP ===
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const text = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = text;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + rect.width/2 - tooltip.offsetWidth/2) + 'px';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// === DRAG AND DROP UPLOAD ===
function initDragDropUpload(dropzoneId, inputId) {
    const dropzone = document.getElementById(dropzoneId);
    const input = document.getElementById(inputId);
    
    if (!dropzone || !input) return;
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.classList.add('highlight');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.classList.remove('highlight');
        });
    });
    
    dropzone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        input.files = files;
        handleFiles(files);
    });
    
    dropzone.addEventListener('click', () => {
        input.click();
    });
}

function handleFiles(files) {
    Array.from(files).forEach(file => {
        console.log('File uploaded:', file.name);
    });
}

// === INITIALIZE ON PAGE LOAD ===
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Initialize tooltips
    initTooltips();
    
    // Highlight active menu
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu a');
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
