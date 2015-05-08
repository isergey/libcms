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
      this.props.onChange(event.target.value);
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
          <Select onChange={this.changeHandle} choices={this.props.choices} />
          {child}
        </div>
      );
    },
    changeHandle: function (value) {
      var _this = this;
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
      this.props.onChange(value);
    }
  });


  var TextInput = React.createClass({
    getDefaultProps: function () {
      return {
        placeholder: '',
        value: '',
        onChange: function () {
        }
      };
    },
    changeHandle: function (event) {
      this.props.onChange(event.target.value);
    },
    render: function () {
      return (
        <input onChange={this.changeHandle} defaultValue={this.props.value} placeholder={this.props.placeholder} />
      );
    }
  });

  var Field = React.createClass({
    getDefaultProps: function () {
      return {
        label: '',
        errors: [],
        input: TextInput,
        inputProps: {},
        onChange: function () {}
      };
    },
    changeHandle: function (value) {
      this.props.onChange({
        name: this.props.name,
        value: value
      });
    },
    render: function () {
      var label = this.props.label ? <label className="control-label">{ this.props.label }</label> : null;
      var helpBlock = this.props.help ? <p className="help-block">{this.props.help}</p> : null;
      var errors = this.props.errors.map(function (error) {
        return (
          <p className="help-block">{error}</p>
        );
      });
      var cx = React.addons.classSet;
      var classes = cx({
        'control-group': true,
        'error': this.props.errors.length > 0
      });

      var inputProps = this.props.inputProps;
      inputProps.onChange = this.changeHandle;

      return (
        <div className={classes}>
          {label}
          <div className="controls">
          {React.createFactory(this.props.input)(inputProps)}
          {helpBlock}
          {errors}
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
        departments: [],
        errors: {}
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
      console.log('libraryChangeHandle', event);
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
    changeHandle: function (event) {
      var values = this.state.values;
      values[event.name] = event.value;
      this.setState({
        values: values
      });
      console.log(event);
    },
    submitHandle: function (event) {
      event.preventDefault();
      console.log(this.state.values);
    },
    render: function () {
      var loader = (<div>Форма загружается...</div>);
      var form = (
        <form onSubmit={this.submitHandle} className="form">
          <Field name="district"
            onChange={this.districtsChangeHandle}
            input={Select}
            inputProps={{
              choices: this.state.districts
            }}
          />
          <Field name="library"
            key={this.state.values.district}
            onChange={this.libraryChangeHandle}
            input={TreeSelect}
            inputProps={{
              choices: this.state.libraries
            }}
          />
          <Field name="department"
            key={this.state.values.library}
            input={TreeSelect}
            inputProps={{
              choices: this.state.departments
            }}
          />
          <Field name='email'
            onChange={this.changeHandle}
            label="Email"
            help="Только в домене @tatar.ru"
            input={TextInput}
            inputProps={{
              placeholder: 'Только в домене @tatar.ru'
            }}/>
          <Field name='first_name'
            label='Имя'
            onChange={this.changeHandle}/>
          <Field name='second_name'
            label='Отчество'
            onChange={this.changeHandle}/>
          <Field name='last_name'
            label='Фамилия'
            onChange={this.changeHandle}/>
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

