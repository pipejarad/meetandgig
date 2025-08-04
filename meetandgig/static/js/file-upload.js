/**
 * Funcionalidad mejorada para subida de archivos de imagen
 * Meet & Gig - Ticket 2.3: Subida de foto de perfil
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidad de subida de archivos
    initFileUpload();
});

function initFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    fileInputs.forEach(function(input) {
        setupFileInput(input);
    });
}

function setupFileInput(input) {
    // Crear contenedor de vista previa si no existe
    const previewContainer = createPreviewContainer(input);
    
    // Manejar cambio de archivo
    input.addEventListener('change', function(e) {
        handleFileChange(e, previewContainer);
    });
    
    // Manejar drag & drop
    const parent = input.closest('.mb-3') || input.parentElement;
    setupDragAndDrop(parent, input);
}

function createPreviewContainer(input) {
    let container = input.parentElement.querySelector('.file-preview-container');
    
    if (!container) {
        container = document.createElement('div');
        container.className = 'file-preview-container mt-2';
        input.parentElement.appendChild(container);
    }
    
    return container;
}

function handleFileChange(event, previewContainer) {
    const file = event.target.files[0];
    
    if (!file) {
        previewContainer.innerHTML = '';
        return;
    }
    
    // Validar archivo
    const validation = validateImageFile(file);
    if (!validation.valid) {
        showFileError(previewContainer, validation.error);
        event.target.value = ''; // Limpiar input
        return;
    }
    
    // Mostrar vista previa
    showImagePreview(file, previewContainer);
}

function validateImageFile(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    
    // Validar tipo
    if (!allowedTypes.includes(file.type)) {
        return {
            valid: false,
            error: 'Solo se permiten archivos JPG, PNG o GIF.'
        };
    }
    
    // Validar tamaño
    if (file.size > maxSize) {
        return {
            valid: false,
            error: 'La imagen no puede ser mayor a 5MB.'
        };
    }
    
    return { valid: true };
}

function showImagePreview(file, container) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            // Validar dimensiones mínimas
            if (this.width < 100 || this.height < 100) {
                showFileError(container, 'La imagen debe tener al menos 100x100 píxeles.');
                return;
            }
            
            // Mostrar vista previa exitosa
            container.innerHTML = `
                <div class="current-file-info">
                    <div class="d-flex align-items-center">
                        <img src="${e.target.result}" alt="Vista previa" class="preview-image me-3">
                        <div>
                            <div class="file-name">
                                <i class="icon-check text-success"></i> ${file.name}
                            </div>
                            <small class="text-muted">
                                ${formatFileSize(file.size)} • ${this.width}×${this.height}px
                            </small>
                        </div>
                    </div>
                </div>
            `;
        };
        img.src = e.target.result;
    };
    
    reader.readAsDataURL(file);
}

function showFileError(container, message) {
    container.innerHTML = `
        <div class="alert alert-danger alert-sm">
            <i class="icon-warning"></i> ${message}
        </div>
    `;
}

function setupDragAndDrop(element, input) {
    // Prevenir comportamiento por defecto
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        element.addEventListener(eventName, preventDefaults, false);
    });
    
    // Highlight en drag over
    ['dragenter', 'dragover'].forEach(eventName => {
        element.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        element.addEventListener(eventName, unhighlight, false);
    });
    
    // Manejar drop
    element.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            input.files = files;
            // Disparar evento change
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        element.classList.add('drag-over');
    }
    
    function unhighlight(e) {
        element.classList.remove('drag-over');
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
