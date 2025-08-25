/**
 * Lecture Video Player with fullscreen, like, and share functionality
 */

class LecturePlayer {
    constructor(options) {
        this.videoElement = options.videoElement;
        this.fullscreenButton = options.fullscreenButton;
        this.likeButton = options.likeButton;
        this.shareButtons = options.shareButtons;
        this.copyUrlButton = options.copyUrlButton;
        this.shareUrlInput = options.shareUrlInput;
        this.lectureId = options.lectureId;
        this.likeCountElement = options.likeCountElement;
        
        this.init();
    }
    
    init() {
        this.setupFullscreen();
        this.setupLikeButton();
        this.setupShareButtons();
        this.setupCopyUrl();
        this.setupVideoEvents();
    }
    
    setupFullscreen() {
        if (!this.fullscreenButton || !this.videoElement) return;
        
        this.fullscreenButton.addEventListener('click', () => {
            if (this.videoElement.requestFullscreen) {
                this.videoElement.requestFullscreen();
            } else if (this.videoElement.webkitRequestFullscreen) { /* Safari */
                this.videoElement.webkitRequestFullscreen();
            } else if (this.videoElement.msRequestFullscreen) { /* IE11 */
                this.videoElement.msRequestFullscreen();
            }
        });
    }
    
    setupLikeButton() {
        if (!this.likeButton || !this.lectureId) return;
        
        this.likeButton.addEventListener('click', () => {
            fetch(`/instructor/lectures/${this.lectureId}/like`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (this.likeCountElement) {
                        this.likeCountElement.textContent = data.likes;
                    }
                    
                    if (data.liked) {
                        this.likeButton.classList.remove('btn-outline-primary');
                        this.likeButton.classList.add('btn-primary');
                    } else {
                        this.likeButton.classList.remove('btn-primary');
                        this.likeButton.classList.add('btn-outline-primary');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
    
    setupShareButtons() {
        if (!this.shareButtons || !this.shareButtons.length || !this.lectureId) return;
        
        const shareUrl = this.shareUrlInput ? this.shareUrlInput.value : window.location.href;
        const lectureTitle = document.querySelector('h2') ? document.querySelector('h2').textContent : 'Lecture';
        
        this.shareButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const platform = button.getAttribute('data-platform');
                
                // Record share action
                fetch(`/instructor/lectures/${this.lectureId}/share`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({ platform: platform })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Open share dialog based on platform
                        let shareLink;
                        switch(platform) {
                            case 'email':
                                shareLink = `mailto:?subject=Check out this lecture: ${encodeURIComponent(lectureTitle)}&body=${encodeURIComponent('I thought you might be interested in this lecture: ' + shareUrl)}`;
                                break;
                            case 'whatsapp':
                                shareLink = `https://wa.me/?text=${encodeURIComponent(lectureTitle + ' ' + shareUrl)}`;
                                break;
                            case 'facebook':
                                shareLink = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
                                break;
                            case 'twitter':
                                shareLink = `https://twitter.com/intent/tweet?text=${encodeURIComponent(lectureTitle)}&url=${encodeURIComponent(shareUrl)}`;
                                break;
                        }
                        
                        if (shareLink) {
                            window.open(shareLink, '_blank');
                        }
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    }
    
    setupCopyUrl() {
        if (!this.copyUrlButton || !this.shareUrlInput) return;
        
        this.copyUrlButton.addEventListener('click', () => {
            this.shareUrlInput.select();
            document.execCommand('copy');
            
            // Show copied tooltip
            const originalIcon = this.copyUrlButton.querySelector('i').className;
            this.copyUrlButton.querySelector('i').className = 'fas fa-check';
            
            setTimeout(() => {
                this.copyUrlButton.querySelector('i').className = originalIcon;
            }, 2000);
        });
    }
    
    setupVideoEvents() {
        if (!this.videoElement) return;
        
        // Track video play events
        this.videoElement.addEventListener('play', () => {
            this.trackVideoEvent('play');
        });
        
        // Track video pause events
        this.videoElement.addEventListener('pause', () => {
            this.trackVideoEvent('pause');
        });
        
        // Track video ended events
        this.videoElement.addEventListener('ended', () => {
            this.trackVideoEvent('ended');
        });
        
        // Track video seeking events
        this.videoElement.addEventListener('seeking', () => {
            this.trackVideoEvent('seeking', { position: this.videoElement.currentTime });
        });
    }
    
    trackVideoEvent(eventType, data = {}) {
        if (!this.lectureId) return;
        
        // Optional: Send video interaction events to server for analytics
        // This is a placeholder for future analytics implementation
        console.log(`Video event: ${eventType}`, data);
    }
}

// Initialize the player when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const videoElement = document.getElementById('lecture-video');
    if (!videoElement) return;
    
    const player = new LecturePlayer({
        videoElement: videoElement,
        fullscreenButton: document.getElementById('fullscreen-btn'),
        likeButton: document.getElementById('like-btn'),
        shareButtons: document.querySelectorAll('.share-btn'),
        copyUrlButton: document.getElementById('copy-url-btn'),
        shareUrlInput: document.getElementById('share-url'),
        lectureId: videoElement.getAttribute('data-lecture-id'),
        likeCountElement: document.getElementById('like-count')
    });
});