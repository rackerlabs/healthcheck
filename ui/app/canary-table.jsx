import React from 'react';
import ResourceTable from './resource-table';

var CanaryTable = React.createClass({

    columnTitles: [
        "Id", "Name", "Status", "Health", "Description"
    ],

    columnKeys: [
        "id", "name", "status", "health", "description"
    ],

    getColumnLinks: function() {
        var project_id = this.props.project_id;
        return {
                 name: function(canary) {
                    return "/projects/" + project_id + "/canary/" + canary.id + "/results";
                 },
                 id: function(canary) {
                    return "/projects/" + project_id + "/canary/" + canary.id + "/results";
                 }
               }
    },

    render: function() {
        return (
            <ResourceTable resources={this.props.canary}
                            columnTitles={this.columnTitles}
                            columnKeys={this.columnKeys}
                            columnLinks={this.getColumnLinks()} />
        );
    }

});

export default CanaryTable;
