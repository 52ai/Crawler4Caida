import React from 'react';
import resource from '../utils/resources.js';
import intl from 'react-intl-universal';

registerDataTemplates();

class windowTitle extends React.Component {
  render() {
    return <ContentControl viewModel={this.props.viewModel} key={this.props.viewModel.id} />;
  }
}

class ContentControl extends React.Component {
  render() {
    var viewModel = this.props.viewModel;
    var Template;

    if (viewModel) {
      Template = contentTemplateSelector(viewModel);
    }
    if (!Template) {
      return <div>{viewModel}</div>;
    }

    return <Template {...viewModel} />;
  };
}

function contentTemplateSelector(type) {
  var typeName = (type && type.__name) ||
                 (type && type.constructor && type.constructor.name);
  if (typeName) {
    return resource(typeName);
  }
}

function registerDataTemplates() {
  resource.add(
    "DegreeWindowViewModel",
    // React class component
    class extends React.Component {
      render() {
        if (this.props.id === undefined) return null;
        return (
          <h4 className="window-title">
            <span className="node-name node-focus" id={this.props.id}>
              {this.props.nodeName}
            </span>
            {/* <span className={this.props.connectionClassName === 'in' ? 'window-indegree' : 'window-outdgree'}> */}
            {/*   {this.props.degreeKindName} */}
            {/* </span> */}
            {intl.getHTML("COUNT_FOR_RELATED_PROJECTS", {
              count: this.props.degreeNumber,
            })}
          </h4>
        );
      }
    }
  );

  resource.add(
    "SearchResultWindowViewModel",
    // React functional component
    (props) => {
      return (
        <h4 className="window-title">
          {intl.getHTML("COUNT_FOR_SEARCH_MATCHES", {
            count: props.matchesCountString,
          })}
        </h4>
      );
    }
  );
}

export default windowTitle;
