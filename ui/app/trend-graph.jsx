import React from 'react';

var TrendGraph = React.createClass({

    getInitialState: function() {
        return {
            graph: "",
        }
    },

    componentDidMount: function() {
        var url = "/api/projects/" + this.props.project_id + "/canary/" + this.props.canary_id +
                  "/trend?interval=30%20days&resolution=1%20days&threshold=50";
        this.canaryRequest = $.get(url, function(result) {
            this.setState({
                graph: result
            })
        }.bind(this))
    },

    componentWillUnmount: function() {
        this.projectsRequest.abort();
    },

    createGraph: function() {
        return {__html: this.state.graph};
    },

    render: function() {
        return (
            <div dangerouslySetInnerHTML={ this.createGraph() } />
        );
    },

});

export default TrendGraph;
