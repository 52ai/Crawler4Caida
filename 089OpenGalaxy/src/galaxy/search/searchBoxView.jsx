import React from 'react';
import searchBoxModel from './searchBoxModel.js';
import intl from 'react-intl-universal';

class searchBar extends React.Component {
  constructor() {
    super();
    this.runSearch = this.runSearch.bind(this);
    this.runSubmit = this.runSubmit.bind(this);
  }
  render() {
    return (
        <div className='search'>
          <form className='search-form' role='search' onSubmit={this.runSubmit}>
            <div className='input-group'>
              <input type='text'
                ref='searchText'
                className='form-control no-shadow' placeholder={intl.get('SEARCH_PLACEHOLDER')}
                onChange={this.runSearch}/>
                <span className='input-group-btn'>
                  <button className='btn' tabIndex='-1' type='button'>
                    <span className='glyphicon glyphicon-search'></span>
                  </button>
                </span>
            </div>
          </form>
        </div>
    );
  };

  runSearch(e) {
    searchBoxModel.search(e.target.value);
  }

  runSubmit(e) {
    var searchText = React.findDOMNode(this.refs.searchText).value;
    searchBoxModel.submit(searchText);
    e.preventDefault();
  }
}

export default searchBar;
