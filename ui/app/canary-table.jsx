import React from 'react';
import ResourceTable from './resource-table';

var BuildsTable = React.createClass({

    columnTitles: [
        "Id", "Name", "Description", "Criteria"
    ],
    columnKeys: [
        "id", "name", "description", "criteria"
    ],
    columnLinks: {
        name: function(canary) {
            return "/projects/" + canary.project_id + "/canary/" + canary.id + "/results";
        },
        id: function(canary) {
            return "/projects/" + canary.project_id + "/canary/" + canary.id + "/results";
        }
    },

    render: function() {
        return (
            <ResourceTable resources={this.props.canary}
                            columnTitles={this.columnTitles}
                            columnKeys={this.columnKeys}
                            columnLinks={this.columnLinks} />
        );
    }

});

export default BuildsTable;
