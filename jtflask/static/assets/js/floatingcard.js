/*global vendors*/
const JTFloatingCard = (() => {
    "use strict";

    let isFloating = false;
    let isDragging = false;
    let offsetX = 0;
    let offsetY = 0;

    const undockCard = (card, dragHandle, undockButton, dockIcon, digitalTwinContainer) => {
        if (!card || !card.parentNode) {
            console.log("No parent node found for the card. Skipping docking logic.");
            return;
        }

        const originalContainer = card.parentNode;
        const originalIndex = Array.prototype.indexOf.call(originalContainer.children, card);

        const toggleDocking = () => {
            if (!isFloating) {
                // Move the card to the digital twin container (floating mode)
                digitalTwinContainer.appendChild(card);
                card.classList.add('floating-card');
                card.classList.remove('docked-card');
                card.style.position = 'absolute'; // Enable absolute positioning for floating
                card.style.zIndex = '1000';  // Ensure it's on top
                isFloating = true;
            } else {
                // Restore the card back to its original container (docked mode)
                if (originalIndex >= 0) {
                    originalContainer.insertBefore(card, originalContainer.children[originalIndex]);
                } else {
                    originalContainer.appendChild(card); // Fallback if index isn't available
                }
                card.classList.remove('floating-card');
                card.classList.add('docked-card');
                dockIcon.setAttribute('data-icon', 'solar:maximize-square-3-outline');  // Switch back to maximize icon
                card.style.position = 'relative'; // Reset position to relative for docked mode
                card.style.zIndex = '';  // Reset z-index
                card.style.left = '';  // Clear the left position
                card.style.top = '';  // Clear the top position
                isFloating = false;
            }
        };

        // Event listener to toggle between docked and floating mode
        undockButton.addEventListener('click', toggleDocking);

        // Mouse down event on the drag handle
        dragHandle.addEventListener('mousedown', (e) => {
            if (isFloating) {
                isDragging = true;
                // Get the current mouse position and calculate the offset
                offsetX = e.clientX - card.getBoundingClientRect().left;
                offsetY = e.clientY - card.getBoundingClientRect().top;
            }
        });

        // Mouse move event to drag the card
        document.addEventListener('mousemove', (e) => {
            if (isDragging && isFloating) {
                // Update card position based on the mouse movement
                card.style.left = `${e.clientX - offsetX}px`;
                card.style.top = `${e.clientY - offsetY}px`;
            }
        });

        // Mouse up event to stop dragging
        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    };

    // Public method to initialize the card with the provided parameters
    return {
        init: (card, dragHandle, undockButton, dockIcon, digitalTwinContainer) => {
            if (card && card.parentNode) {
                undockCard(card, dragHandle, undockButton, dockIcon, digitalTwinContainer);
            } else {
                console.log("Card or parent node not found. Docking logic skipped.");
            }
        }
    };
})();  // IIFE


