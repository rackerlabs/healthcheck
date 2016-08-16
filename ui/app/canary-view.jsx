import React from 'react';
import CanaryTable from './canary-table';

var CanaryView = React.createClass({

    getInitialState: function() {
        return {
            canary: [],
        }
    },

    projectId: function() {
        return this.props.params.project_id || this.props.project_id;
    },

    componentDidMount: function() {
        var url = "/api/projects/" + this.projectId() + "/canary";
        this.canaryRequest = $.get(url, function(result) {
            this.setState({
                canary: result.canaries
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.canaryRequest.abort();
    },

    render: function() {
        return (
            <div>
                <h2 className="rs-page-title">Canaries</h2>
                <CanaryTable canary={this.state.canary} project_id={this.projectId()} />
            </div>
        );
    },
});

export default CanaryView;
