/**
 * Checkboxer - A utility to manage checkbox states in the opportunity visualization
 * 
 * This script is injected into the visualization HTML to handle the initial state
 * of checkboxes based on team configuration. It ensures that:
 * 1. All checkboxes are initially turned off
 * 2. Only team-relevant checkboxes are turned on
 * 3. The visualization updates to reflect these changes
 */

class Checkboxer {
    /**
     * Initialize the checkboxer with team configuration
     * @param {Object} config - The team configuration from the server
     */
    constructor(config) {
        this.config = config || {};
        this.initialized = false;
        
        // Wait for the visualization to be ready
        this.initializeWhenReady();
    }

    /**
     * Wait for the visualization and checkboxes to be ready before initializing
     */
    initializeWhenReady() {
        // Check if Plotly is loaded and the plot div exists
        if (typeof Plotly === 'undefined' || !document.getElementById('plotly-div')) {
            setTimeout(() => this.initializeWhenReady(), 100);
            return;
        }
        
        // Check if checkboxes are present in the DOM
        const checkboxes = document.querySelectorAll('.prop-checkbox, .funder-checkbox');
        if (checkboxes.length === 0) {
            console.log('Waiting for checkboxes to be rendered...');
            setTimeout(() => this.initializeWhenReady(), 100);
            return;
        }
        
        console.log('All checkboxes found in DOM, initializing...');
        this.initialize();
    }

    /**
     * Initialize the checkboxer
     */
    initialize() {
        if (this.initialized) return;
        this.initialized = true;
        
        console.log('Initializing Checkboxer with config:', this.config);
        
        // Wait for the plot to be fully rendered
        const checkPlot = () => {
            const plotDiv = document.getElementById('plotly-div');
            if (!plotDiv || !plotDiv._fullLayout) {
                setTimeout(checkPlot, 100);
                return;
            }
            
            this.setInitialCheckboxStates();
        };
        
        checkPlot();
    }

    /**
     * Set the initial states of all checkboxes
     */
    setInitialCheckboxStates() {
        console.log('setInitialCheckboxStates called with config:', this.config);
        
        // Turn off all checkboxes first
        console.log('Turning off all checkboxes...');
        this.toggleAllCheckboxes('prop', false);
        this.toggleAllCheckboxes('funder', false);

        // If we have team configuration, turn on the relevant checkboxes
        if (this.config.initial_propositions && this.config.initial_propositions.length > 0) {
            console.log('Setting initial propositions:', this.config.initial_propositions);
            this.config.initial_propositions.forEach(prop => {
                console.log('Enabling proposition checkbox:', prop);
                this.toggleCheckbox('prop', prop, true);
            });
        } else {
            console.log('No initial propositions configured');
        }

        if (this.config.initial_funders && this.config.initial_funders.length > 0) {
            console.log('Setting initial funders:', this.config.initial_funders);
            this.config.initial_funders.forEach(funder => {
                console.log('Enabling funder checkbox:', funder);
                this.toggleCheckbox('funder', funder, true);
            });
        } else {
            console.log('No initial funders configured');
        }

        // Log the final state of all checkboxes
        setTimeout(() => {
            console.log('Final checkbox states:');
            console.log('Propositions:');
            document.querySelectorAll('.prop-checkbox').forEach(cb => {
                console.log(`- ${cb.dataset.name}: ${cb.checked ? 'checked' : 'unchecked'}`);
            });
            console.log('Funders:');
            document.querySelectorAll('.funder-checkbox').forEach(cb => {
                console.log(`- ${cb.dataset.name}: ${cb.checked ? 'checked' : 'unchecked'}`);
            });
        }, 100);

        // Trigger the plot update
        console.log('Triggering plot update...');
        this.triggerPlotUpdate();
    }

    /**
     * Toggle all checkboxes of a given type
     * @param {string} type - 'prop' or 'funder'
     * @param {boolean} state - The state to set
     */
    toggleAllCheckboxes(type, state) {
        const checkboxes = document.querySelectorAll(`.${type}-checkbox`);
        checkboxes.forEach(checkbox => {
            checkbox.checked = state;
        });
        
        // Update the 'All' checkbox state
        const allCheckbox = document.getElementById(`toggleAll${this.capitalize(type)}s`);
        if (allCheckbox) {
            allCheckbox.checked = state;
            allCheckbox.indeterminate = false;
        }
    }

    /**
     * Toggle a specific checkbox
     * @param {string} type - 'prop' or 'funder'
     * @param {string} name - The name of the item
     * @param {boolean} state - The state to set
     */
    toggleCheckbox(type, name, state) {
        const selector = `.${type}-checkbox[data-name="${this.escapeCssSelector(name)}"]`;
        console.log(`Toggling ${type} checkbox:`, { name, state, selector });
        const checkbox = document.querySelector(selector);
        if (checkbox) {
            console.log(`Found checkbox for ${name}, setting checked=${state}`);
            checkbox.checked = state;
            // Trigger change event to ensure any listeners are notified
            const event = new Event('change');
            checkbox.dispatchEvent(event);
        } else {
            console.warn(`Could not find checkbox for ${type}:`, name);
        }
    }

    /**
     * Trigger the plot to update based on current checkbox states
     */
    triggerPlotUpdate() {
        // Find and trigger the update function
        const updateFunc = window.updatePlotVisibility;
        if (typeof updateFunc === 'function') {
            updateFunc();
        } else {
            console.warn('Could not find updatePlotVisibility function');
        }
    }

    /**
     * Helper to capitalize the first letter of a string
     */
    capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    /**
     * Escape special characters in CSS selectors
     */
    escapeCssSelector(selector) {
        return selector.replace(/[ !"#$%&'()*+,.\/:;<=>?@\[\]^`{|}~]/g, '\\$&');
    }
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Checkboxer;
}
