import React, { ChangeEvent, Component } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import * as actions from "../../store/actions";
import { connect } from "react-redux";
import { ConnectState } from "../../interfaces";

class DetailsForm extends Component<any> {
  private formFieldOnChangeHandler = (event: ChangeEvent) => {
    const elem = event.target as HTMLInputElement;
    let storeRef = elem.id.replace(/^form/, "");
    storeRef = storeRef.charAt(0).toLowerCase() + storeRef.slice(1);
    const value = elem.value;
    this.props.onUpdateForm({ [storeRef]: value });
  };

  render() {
    return (
      <div>
        <h1>Form Details</h1>
        <Form.Group controlId="formTitle">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter title"
            required
            value={this.props.form.title}
            onChange={this.formFieldOnChangeHandler}
          />
        </Form.Group>

        <Form.Group controlId="formDescription">
          <Form.Label>Description</Form.Label>
          <CKEditor
            editor={ClassicEditor}
            data={this.props.form.description}
            onChange={(_: any, editor: { getData: () => any }) => {
              const data = editor.getData();
              this.props.onUpdateForm({ description: data });
            }}
          />
        </Form.Group>

        <Form.Group controlId="formStartDt">
          <Form.Label>Start Date</Form.Label>
          <Form.Control
            type="datetime-local"
            placeholder="Enter start date and time"
            value={this.props.form.startDt}
            onChange={this.formFieldOnChangeHandler}
          />
        </Form.Group>

        <Form.Group controlId="formEndDt">
          <Form.Label>End Date</Form.Label>
          <Form.Control
            type="datetime-local"
            placeholder="Enter end date and time"
            value={this.props.form.endDt}
            onChange={this.formFieldOnChangeHandler}
          />
        </Form.Group>

        <Form.Group controlId="formSubmit">
          <Button
            variant="primary"
            type="submit"
            onClick={this.props.onSubmit}
          >
            Submit
          </Button>
        </Form.Group>
      </div>
    );
  }
}

const mapStateToProps = (state: ConnectState) => {
  return {
    form: state.formSetup.form,
  };
};

const mapDispatchToProps = (dispatch: any) => {
  return {
    onUpdateForm: (formFields: { [field: string]: any }) =>
      dispatch(actions.updateForm(formFields)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(DetailsForm);
