import React from 'react';
import ResourceTable from './resource-table';

var ResultsTable = React.createClass({

    columnTitles: [
        "Id", "Created At", "Status", "Failure Details",

    ],
    columnKeys: [
        "id", "created_at", "status", "failure_details",
    ],
    columnLinks: {
        project_id: function(r) {
            return "/projects/" + r.project_id + "/canary";
        },
    },

    render: function() {
        return (
            <ResourceTable resources={this.props.results}
                            columnTitles={this.columnTitles}
                            columnKeys={this.columnKeys}
                            columnLinks={this.columnLinks} />
        );
    },

});

export default ResultsTable;
