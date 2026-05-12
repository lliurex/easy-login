import QtQuick
import QtQml.Models

DelegateModel {
    id: filterModel

    property var externalTimer: null
    property string role: ""
    property string search: ""
    property var visibleElements: []

    filterOnGroup: "visible"

    groups: [
        DelegateModelGroup {
            id: allItems
            name: "all"
            includeByDefault: true
        },
        DelegateModelGroup {
            id: visibleItems
            name: "visible"
            includeByDefault: true
        }
    ]

    function update() {
        if (!items || items.count <= 0) return;

        let searchLower = search.toLowerCase();
        let tempVisibleIndices = [];

        for (let i = 0; i < items.count; i++) {

            let itemHandle = items.get(i);
            let itemData = itemHandle.model;
            
            let val = itemData[role];
            let matches = (searchLower === "") || 
                          (val !== undefined && val !== null && 
                           val.toString().toLowerCase().includes(searchLower));

            itemHandle.inVisible = matches;

            if (matches) {
                tempVisibleIndices.push(i);
            }
        }
        visibleElements = tempVisibleIndices;
    }

    onSearchChanged: if (externalTimer) externalTimer.restart()
    onRoleChanged: if (externalTimer) externalTimer.restart()
    Component.onCompleted: if (externalTimer) externalTimer.restart()
}
