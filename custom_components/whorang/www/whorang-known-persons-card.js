/**
 * WhoRang Known Persons Card
 * Custom Lovelace card for displaying known persons with avatars
 */

class WhoRangKnownPersonsCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.persons = [];
    this.isLoading = false;
  }

  setConfig(config) {
    this.config = {
      entity: 'sensor.whorang_known_persons_gallery',
      title: 'Known Persons',
      columns: 3,
      show_stats: true,
      show_last_seen: true,
      show_face_count: true,
      whorang_url: null,
      ...config
    };
    this.render();
  }

  set hass(hass) {
    this._hass = hass;
    this.updatePersons();
  }

  updatePersons() {
    if (!this._hass) return;
    
    const gallery = this._hass.states[this.config.entity];
    if (gallery && gallery.attributes) {
      const persons = gallery.attributes.persons || [];
      const totalKnown = gallery.attributes.total_known_persons || 0;
      const totalFaces = gallery.attributes.total_labeled_faces || 0;
      const avgFaces = gallery.attributes.avg_faces_per_person || 0;
      const galleryReady = gallery.attributes.gallery_ready || false;
      const backendUrl = gallery.attributes.backend_url || this.config.whorang_url;
      
      // Only update if data has changed
      if (JSON.stringify(this.persons) !== JSON.stringify(persons)) {
        this.persons = persons;
        this.totalKnown = totalKnown;
        this.totalFaces = totalFaces;
        this.avgFaces = avgFaces;
        this.galleryReady = galleryReady;
        this.backendUrl = backendUrl;
        this.renderContent();
      }
    }
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
        }
        
        .known-persons {
          background: var(--card-background-color, #fff);
          border-radius: 12px;
          box-shadow: var(--ha-card-box-shadow, 0 2px 8px rgba(0,0,0,0.1));
          padding: 16px;
          font-family: var(--paper-font-body1_-_font-family);
        }
        
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }
        
        .title {
          font-size: 1.2em;
          font-weight: 500;
          color: var(--primary-text-color, #212121);
          margin: 0;
        }
        
        .stats-info {
          font-size: 0.9em;
          color: var(--secondary-text-color, #757575);
          text-align: right;
        }
        
        .stats-summary {
          background: var(--secondary-background-color, #f5f5f5);
          border-radius: 8px;
          padding: 12px;
          margin-bottom: 16px;
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 12px;
        }
        
        .stat-item {
          text-align: center;
        }
        
        .stat-value {
          font-size: 1.5em;
          font-weight: bold;
          color: var(--primary-color, #03a9f4);
          display: block;
        }
        
        .stat-label {
          font-size: 0.8em;
          color: var(--secondary-text-color, #757575);
          margin-top: 4px;
        }
        
        .persons-grid {
          display: grid;
          grid-template-columns: repeat(var(--columns, 3), 1fr);
          gap: 16px;
          margin-bottom: 16px;
        }
        
        @media (max-width: 768px) {
          .persons-grid {
            grid-template-columns: repeat(2, 1fr);
          }
        }
        
        @media (max-width: 480px) {
          .persons-grid {
            grid-template-columns: 1fr;
          }
        }
        
        .person-card {
          background: var(--card-background-color, #fff);
          border: 1px solid var(--divider-color, #e0e0e0);
          border-radius: 12px;
          padding: 16px;
          text-align: center;
          transition: all 0.2s ease;
          cursor: pointer;
          position: relative;
          overflow: hidden;
        }
        
        .person-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          border-color: var(--primary-color, #03a9f4);
        }
        
        .avatar-container {
          position: relative;
          width: 80px;
          height: 80px;
          margin: 0 auto 12px;
          border-radius: 50%;
          overflow: hidden;
          background: var(--secondary-background-color, #f5f5f5);
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .avatar-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
          border-radius: 50%;
        }
        
        .avatar-placeholder {
          width: 40px;
          height: 40px;
          color: var(--secondary-text-color, #757575);
          font-size: 40px;
        }
        
        .avatar-loading {
          width: 24px;
          height: 24px;
          border: 2px solid var(--divider-color, #e0e0e0);
          border-top: 2px solid var(--primary-color, #03a9f4);
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        
        .face-count-badge {
          position: absolute;
          top: -4px;
          right: -4px;
          background: var(--primary-color, #03a9f4);
          color: white;
          border-radius: 50%;
          width: 24px;
          height: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.7em;
          font-weight: bold;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .person-name {
          font-size: 1em;
          font-weight: 500;
          color: var(--primary-text-color, #212121);
          margin-bottom: 8px;
          word-break: break-word;
        }
        
        .person-details {
          font-size: 0.8em;
          color: var(--secondary-text-color, #757575);
          line-height: 1.4;
        }
        
        .detail-row {
          display: flex;
          justify-content: space-between;
          margin-bottom: 4px;
        }
        
        .detail-label {
          font-weight: 500;
        }
        
        .last-seen {
          color: var(--success-color, #4caf50);
        }
        
        .last-seen.old {
          color: var(--warning-color, #ff9800);
        }
        
        .last-seen.very-old {
          color: var(--error-color, #f44336);
        }
        
        .empty-state {
          text-align: center;
          padding: 40px 20px;
          color: var(--secondary-text-color, #757575);
        }
        
        .empty-state .icon {
          font-size: 48px;
          margin-bottom: 16px;
          opacity: 0.5;
        }
        
        .loading-state {
          text-align: center;
          padding: 40px 20px;
          color: var(--secondary-text-color, #757575);
        }
        
        .error-state {
          text-align: center;
          padding: 40px 20px;
          color: var(--error-color, #f44336);
          background: var(--error-color, #f44336)10;
          border-radius: 8px;
          margin: 16px 0;
        }
        
        .controls {
          display: flex;
          justify-content: center;
          gap: 12px;
          margin-top: 16px;
        }
        
        .control-btn {
          padding: 8px 16px;
          border: 1px solid var(--primary-color, #03a9f4);
          background: transparent;
          color: var(--primary-color, #03a9f4);
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.9em;
          transition: all 0.2s ease;
        }
        
        .control-btn:hover {
          background: var(--primary-color, #03a9f4);
          color: white;
        }
        
        .control-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        .person-card.active {
          border-color: var(--primary-color, #03a9f4);
          background: var(--primary-color, #03a9f4)08;
        }
        
        .confidence-indicator {
          position: absolute;
          bottom: 8px;
          right: 8px;
          background: rgba(0,0,0,0.7);
          color: white;
          padding: 2px 6px;
          border-radius: 4px;
          font-size: 0.7em;
        }
        
        .confidence-high {
          background: rgba(76, 175, 80, 0.8);
        }
        
        .confidence-medium {
          background: rgba(255, 152, 0, 0.8);
        }
        
        .confidence-low {
          background: rgba(244, 67, 54, 0.8);
        }
      </style>
      
      <div class="known-persons">
        <div class="header">
          <h3 class="title">${this.config.title}</h3>
          <div class="stats-info" id="stats-info"></div>
        </div>
        
        <div class="stats-summary" id="stats-summary" style="display: none;">
          <div class="stat-item">
            <span class="stat-value" id="total-persons">0</span>
            <div class="stat-label">Known Persons</div>
          </div>
          <div class="stat-item">
            <span class="stat-value" id="total-faces">0</span>
            <div class="stat-label">Total Faces</div>
          </div>
          <div class="stat-item">
            <span class="stat-value" id="avg-faces">0</span>
            <div class="stat-label">Avg per Person</div>
          </div>
        </div>
        
        <div class="persons-grid" id="persons-grid" style="--columns: ${this.config.columns}"></div>
        
        <div class="controls" id="controls" style="display: none;">
          <button class="control-btn" id="refresh-btn">Refresh Gallery</button>
          <button class="control-btn" id="manage-btn">Manage Persons</button>
        </div>
      </div>
    `;
    
    this.setupEventListeners();
    this.renderContent();
  }

  renderContent() {
    if (!this.shadowRoot) return;
    
    const statsInfo = this.shadowRoot.getElementById('stats-info');
    const statsSummary = this.shadowRoot.getElementById('stats-summary');
    const controls = this.shadowRoot.getElementById('controls');
    
    // Update stats display
    if (this.config.show_stats && this.galleryReady) {
      statsSummary.style.display = 'grid';
      statsInfo.textContent = `${this.totalKnown} persons, ${this.totalFaces} faces`;
      
      this.shadowRoot.getElementById('total-persons').textContent = this.totalKnown;
      this.shadowRoot.getElementById('total-faces').textContent = this.totalFaces;
      this.shadowRoot.getElementById('avg-faces').textContent = this.avgFaces;
    } else {
      statsSummary.style.display = 'none';
      statsInfo.textContent = this.galleryReady ? `${this.totalKnown} known persons` : 'Loading...';
    }
    
    // Show/hide controls
    if (this.persons.length > 0) {
      controls.style.display = 'flex';
    } else {
      controls.style.display = 'none';
    }
    
    this.renderPersonsGrid();
  }

  getWhoRangBaseUrlCandidates() {
    const candidates = [];
    
    // 1. User-configured URL (highest priority)
    if (this.config.whorang_url) {
      candidates.push(this.config.whorang_url.replace(/\/$/, ''));
    }
    
    // 2. Integration-provided URL from entity attributes
    if (this._hass && this.config.entity) {
      const entity = this._hass.states[this.config.entity];
      if (entity?.attributes?.backend_url) {
        candidates.push(entity.attributes.backend_url.replace(/\/$/, ''));
      }
      if (entity?.attributes?.whorang_server_url) {
        candidates.push(entity.attributes.whorang_server_url.replace(/\/$/, ''));
      }
    }
    
    // 3. Smart detection based on current window location
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    
    // Same host with different protocols and ports
    candidates.push(`${protocol}//${hostname}:3001`);
    if (protocol === 'https:') {
      candidates.push(`http://${hostname}:3001`);
    }
    
    // 4. Common Home Assistant configurations
    if (hostname !== 'homeassistant.local') {
      candidates.push('http://homeassistant.local:3001');
    }
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      candidates.push('http://localhost:3001');
      candidates.push('http://127.0.0.1:3001');
    }
    
    // 5. Additional fallback URLs from config
    if (this.config.fallback_urls && Array.isArray(this.config.fallback_urls)) {
      candidates.push(...this.config.fallback_urls.map(url => url.replace(/\/$/, '')));
    }
    
    // Remove duplicates while preserving order
    return [...new Set(candidates)];
  }

  async testImageUrl(url) {
    return new Promise((resolve) => {
      const img = new Image();
      const timeout = setTimeout(() => {
        resolve(false);
      }, 2000); // 2 second timeout
      
      img.onload = () => {
        clearTimeout(timeout);
        resolve(true);
      };
      
      img.onerror = () => {
        clearTimeout(timeout);
        resolve(false);
      };
      
      img.src = url;
    });
  }

  async getWorkingAvatarUrl(person) {
    // First try direct avatar URL from person data
    if (person.avatar_url) {
      if (await this.testImageUrl(person.avatar_url)) {
        return person.avatar_url;
      }
    }
    
    // Try multiple avatar URL patterns
    const baseUrls = this.getWhoRangBaseUrlCandidates();
    
    for (const baseUrl of baseUrls) {
      // Try different avatar endpoint patterns
      const avatarPatterns = [
        `${baseUrl}/api/faces/persons/${person.id}/avatar`,  // Our new pattern
        `${baseUrl}/api/persons/${person.id}/avatar`,        // Current backend pattern
        `${baseUrl}/api/persons/${person.id}/image`,         // Alternative pattern
        `${baseUrl}/api/persons/${person.id}/thumbnail`      // Another alternative
      ];
      
      for (const avatarUrl of avatarPatterns) {
        if (await this.testImageUrl(avatarUrl)) {
          // Cache the working base URL for future use
          this._workingBaseUrl = baseUrl;
          return avatarUrl;
        }
      }
    }
    
    return null; // No avatar available - will show placeholder
  }

  renderPersonsGrid() {
    const grid = this.shadowRoot.getElementById('persons-grid');
    
    if (!this.galleryReady) {
      grid.innerHTML = `
        <div class="loading-state" style="grid-column: 1 / -1;">
          <div class="avatar-loading" style="margin: 0 auto 16px;"></div>
          <div>Loading known persons...</div>
        </div>
      `;
      return;
    }
    
    if (this.persons.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="icon">👥</div>
          <div>No known persons yet</div>
          <div style="margin-top: 8px; font-size: 0.9em;">Start labeling faces to build your person gallery.</div>
        </div>
      `;
      return;
    }
    
    grid.innerHTML = '';
    
    this.persons.forEach(async (person) => {
      const personCard = document.createElement('div');
      personCard.className = 'person-card';
      personCard.dataset.personId = person.id;
      
      // Calculate last seen status
      const lastSeenClass = this.getLastSeenClass(person.last_seen);
      const lastSeenText = this.formatLastSeen(person.last_seen);
      
      // Calculate confidence level
      const confidence = person.avg_confidence || 0;
      const confidenceClass = confidence > 0.8 ? 'confidence-high' : 
                             confidence > 0.6 ? 'confidence-medium' : 'confidence-low';
      
      personCard.innerHTML = `
        <div class="avatar-container">
          <div class="avatar-loading"></div>
          <img class="avatar-image" alt="${person.name}" style="display: none;" />
          <div class="avatar-placeholder" style="display: none;">👤</div>
          ${this.config.show_face_count ? `<div class="face-count-badge">${person.face_count || 0}</div>` : ''}
        </div>
        <div class="person-name">${person.name}</div>
        <div class="person-details">
          ${this.config.show_last_seen && person.last_seen ? `
            <div class="detail-row">
              <span class="detail-label">Last seen:</span>
              <span class="last-seen ${lastSeenClass}">${lastSeenText}</span>
            </div>
          ` : ''}
          <div class="detail-row">
            <span class="detail-label">Faces:</span>
            <span>${person.face_count || 0}</span>
          </div>
          ${person.recognition_count ? `
            <div class="detail-row">
              <span class="detail-label">Recognized:</span>
              <span>${person.recognition_count}x</span>
            </div>
          ` : ''}
        </div>
        ${confidence > 0 ? `<div class="confidence-indicator ${confidenceClass}">${Math.round(confidence * 100)}%</div>` : ''}
      `;
      
      const img = personCard.querySelector('.avatar-image');
      const loading = personCard.querySelector('.avatar-loading');
      const placeholder = personCard.querySelector('.avatar-placeholder');
      
      // Try to get a working avatar URL
      try {
        const workingUrl = await this.getWorkingAvatarUrl(person);
        
        if (workingUrl) {
          img.src = workingUrl;
          
          img.onload = () => {
            loading.style.display = 'none';
            img.style.display = 'block';
          };
          
          img.onerror = () => {
            loading.style.display = 'none';
            placeholder.style.display = 'flex';
          };
        } else {
          // No working URL found
          loading.style.display = 'none';
          placeholder.style.display = 'flex';
        }
      } catch (error) {
        console.error(`Failed to load avatar for person ${person.id}:`, error);
        loading.style.display = 'none';
        placeholder.style.display = 'flex';
      }
      
      personCard.addEventListener('click', () => this.handlePersonClick(person));
      grid.appendChild(personCard);
    });
  }

  getLastSeenClass(lastSeen) {
    if (!lastSeen) return '';
    
    const now = new Date();
    const seenDate = new Date(lastSeen);
    const daysDiff = (now - seenDate) / (1000 * 60 * 60 * 24);
    
    if (daysDiff < 1) return '';
    if (daysDiff < 7) return '';
    if (daysDiff < 30) return 'old';
    return 'very-old';
  }

  formatLastSeen(lastSeen) {
    if (!lastSeen) return 'Never';
    
    const now = new Date();
    const seenDate = new Date(lastSeen);
    const diffMs = now - seenDate;
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    
    if (diffMinutes < 1) return 'Just now';
    if (diffMinutes < 60) return `${diffMinutes}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)}mo ago`;
    return `${Math.floor(diffDays / 365)}y ago`;
  }

  handlePersonClick(person) {
    // Show person details or navigate to person management
    console.log('Person clicked:', person);
    
    // Fire custom event for person selection
    this.dispatchEvent(new CustomEvent('person-selected', {
      detail: { person },
      bubbles: true,
      composed: true
    }));
    
    // You could also open a more detailed view or navigate to person management
    // For now, we'll just highlight the selected person
    this.shadowRoot.querySelectorAll('.person-card').forEach(card => {
      card.classList.remove('active');
    });
    
    const clickedCard = this.shadowRoot.querySelector(`[data-person-id="${person.id}"]`);
    if (clickedCard) {
      clickedCard.classList.add('active');
    }
  }

  setupEventListeners() {
    const refreshBtn = this.shadowRoot.getElementById('refresh-btn');
    const manageBtn = this.shadowRoot.getElementById('manage-btn');

    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => this.refreshGallery());
    }

    if (manageBtn) {
      manageBtn.addEventListener('click', () => this.openPersonManagement());
    }
  }

  refreshGallery() {
    if (!this._hass) return;
    
    try {
      this._hass.callService('homeassistant', 'update_entity', {
        entity_id: this.config.entity
      });
      
      // Show loading state briefly
      const statsInfo = this.shadowRoot.getElementById('stats-info');
      const originalText = statsInfo.textContent;
      statsInfo.textContent = 'Refreshing...';
      
      setTimeout(() => {
        if (statsInfo.textContent === 'Refreshing...') {
          statsInfo.textContent = originalText;
        }
      }, 2000);
      
    } catch (error) {
      console.error('Failed to refresh gallery:', error);
    }
  }

  openPersonManagement() {
    // This could open a dialog or navigate to a person management page
    console.log('Open person management');
    
    // Fire custom event for person management
    this.dispatchEvent(new CustomEvent('person-management-requested', {
      bubbles: true,
      composed: true
    }));
  }

  getCardSize() {
    const personCount = this.persons.length;
    if (personCount === 0) return 3;
    
    const rows = Math.ceil(personCount / this.config.columns);
    const baseSize = this.config.show_stats ? 4 : 3; // +1 for stats summary
    return Math.min(rows + baseSize, 12); // Max 12 rows
  }
}

// Register the custom element
customElements.define('whorang-known-persons-card', WhoRangKnownPersonsCard);

// Register with Lovelace
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'whorang-known-persons-card',
  name: 'WhoRang Known Persons',
  description: 'Display known persons with avatars and statistics',
  preview: true,
  documentationURL: 'https://github.com/Beast12/whorang-addon'
});

console.info(
  '%c WHORANG-KNOWN-PERSONS-CARD %c v1.0.0 ',
  'color: orange; font-weight: bold; background: black',
  'color: white; font-weight: bold; background: dimgray'
);
