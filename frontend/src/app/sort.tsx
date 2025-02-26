const updateDestinationOrder = async (newOrder: number[]) => {
    const response = await fetch('/reorder_destinations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ new_order: newOrder })
    });

    if (response.ok) {
        console.log("Sortierung erfolgreich gespeichert!");
    } else {
        console.error("Fehler beim Speichern der Sortierung");
    }
};