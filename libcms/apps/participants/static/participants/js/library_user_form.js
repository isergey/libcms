'use strict';

/*
 var Field = React.createClass({
 getDefaultProps: function () {
 return {
 label: ''
 };
 },
 render: function () {
 var label = this.props.label === '' ? <label className="control-label">{ this.props.label}</label> : null;
 return (
 <div className="control-group">
 { label }
 <div className="controls">
 { this.props.children}
 </div>
 </div>
 );
 }
 });

 var LibraryUserForm = React.createClass({
 render: function () {
 return (
 <form class="bs-docs-example form-horizontal">
 <Field name='email' label='123' initial="1234@initial">
 <input type="password" id="inputPassword" placeholder="Password" />
 </Field>
 <div class="control-group">
 <div class="controls">
 <button type="submit" class="btn">Sign in</button>
 </div>
 </div>
 </form>
 );
 }
 });*/

(function () {
  var libraryUserAppConfig = window.libraryUserAppConfig;

  var API = {
    getDistricts: function () {
      var defer = $.Deferred();
      $.get(libraryUserAppConfig.districtsUrl).done(function (districtList) {
        var districtsChoices = [];
        districtList.forEach(function (district) {
          districtsChoices.push([
            district.pk,
            district.fields.name
          ]);
        });
        defer.resolve(districtsChoices);
      }).error(function (error) {
        console.log(error);
        defer.reject(error);
      });
      return defer;
    },
    getLibraries: function (options) {
      var defer = $.Deferred();
      $.get(libraryUserAppConfig.librariesURL, options).done(function (data) {
        defer.resolve(data);
      }).error(function (error) {
        console.log(error);
        defer.reject(error);
      });
      return defer;
    },
    getDepartments: function (options) {
      var defer = $.Deferred();
      $.get(libraryUserAppConfig.departmentsURL, options).done(function (data) {
        defer.resolve(data);
      }).error(function (error) {
        console.log(error);
        defer.reject(error);
      });
      return defer;
    }
  };


  var Utils = {
    makeLibraryChoices: function (libraryList) {
      var choices = libraryList.map(function (library) {
        return [library.id, library.name];
      });
      return choices;
    },
    makeDistrictChoices: function (districtList) {
      return districtList;
    }
  };

  var Select = React.createClass({
    getDefaultProps: function () {
      return {
        hasEmpty: true,
        choices: [],
        onChange: function () {
        }
      };
    },
    onChangeHandle: function (event) {
      this.props.onChange({
        name: this.props.name,
        value: event.target.value
      });
    },
    render: function () {
      var options = this.props.choices.map(function (choice) {
        return (<option value={choice[0]}>{choice[1]}</option>);
      });
      if (this.props.hasEmpty) {
        options.unshift(<option value="">----</option>);
      }
      return (
        <select onChange={this.onChangeHandle}>
          {options}
        </select>
      );
    }
  });

  var TreeSelect = React.createClass({
    getDefaultProps: function () {
      return {
        hasEmpty: true,
        choices: [],
        onChange: function () {
        }
      };
    },
    getInitialState: function () {
      return {
        value: '',
        childChoices: []
      };
    },
    render: function () {
      var child = this.state.childChoices.length > 0 ? <TreeSelect name={this.props.name} onChange={this.props.onChange} key={this.state.value} choices={this.state.childChoices } /> : null;
      return (
        <div>
          <Select name={this.props.name} onChange={this.onChangeHandle} choices={this.props.choices} />
          {child}
        </div>
      );
    },
    onChangeHandle: function (event) {
      var _this = this;
      var value = event.value;
      if (value !== '') {
        API.getLibraries({
          'parent_id': value
        }).done(function (libraries) {
          var choices = Utils.makeLibraryChoices(libraries);
          _this.setState({
            value: value,
            childChoices: choices
          });
        });
      } else {
        _this.setState({
          value: '',
          childChoices: []
        });
      }
      this.props.onChange(event);
    }
  });


  //var TextInput = React.createClass({
  //  render: function () {
  //
  //  }
  //});


  var Field = React.createClass({
    render: function () {
      var label = this.props.label ? <label className="control-label">{ this.props.label }</label> : null;
      return (
        <div className="control-group">
          {label}
          <div class="controls">
          {this.props.children}
          </div>
        </div>
      );
    }
  });


  var Form = React.createClass({
    getInitialState: function () {
      return {
        loaded: false,
        values: {},
        libraries: [],
        departments: []
      };
    },
    componentDidMount: function () {
      var _this = this;
      var librariesDefer = API.getLibraries();
      var districtsDefer = API.getDistricts();

      $.when(librariesDefer, districtsDefer).done(function (libraries, districts) {
        _this.setState({
          loaded: true,
          libraries: Utils.makeLibraryChoices(libraries),
          districts: Utils.makeDistrictChoices(districts)
        });
      });
    },
    libraryChangeHandle: function (event) {
      var _this = this;
      if (event.value !== '') {
        API.getDepartments({
          'library_id': event.value
        }).done(function (departamentList) {
          var choices = departamentList.map(function (item) {
            return [item.pk, item.fields.name];
          });
          var values = _this.state.values;
          values.library = event.value;
          _this.setState({
            values: values,
            departments: choices
          });
        });
      } else {
        var values1 = _this.state.values;
        values1.library = '';
        this.setState({
          values: values1,
          departments: []
        });
      }
    },
    districtsChangeHandle: function (event) {
      var _this = this;
      API.getLibraries({
        'district_id': event.value
      }).done(function (libraries) {
        var values = _this.state.values;
        values.district = event.value;
        values.library = '';
        _this.setState({
          values: values,
          libraries: Utils.makeLibraryChoices(libraries)
        });
      });
    },
    render: function () {
      var loader = (<div>Форма загружается...</div>);
      var form = (
        <form className="form">
          <Field label="Район">
            <Select name='districts' onChange={this.districtsChangeHandle} choices={this.state.districts} />
          </Field>
          <Field label="Организация">
            <TreeSelect key={this.state.values.district} name='libraries'  onChange={this.libraryChangeHandle} choices={this.state.libraries} />
          </Field>
          <Field label="Отдел">
            <Select key={this.state.values.library} name='departments' choices={this.state.departments} />
          </Field>
        </form>
      );
      return this.state.loaded ? form : loader;
    }
  });

  $(function () {
    React.render(
      <Form/>,
      $('.library_user_app')[0]
    );
  });
})();

