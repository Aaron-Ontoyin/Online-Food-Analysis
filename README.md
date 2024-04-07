# Online Food Data Explorer

This is a Streamlit application that predicts customer feedback  based on various user inputs. It also provides an interface for an extensive exploration of the data.

## Features

The application takes the following inputs from the user:

- Age
- Gender
- Marital Status
- Occupation
- Monthly Income
- Educational Qualifications
- Family Size
- Latitude
- Longitude
- Delivery Status

Based on these inputs, the application predicts whether the customer feedback would be Positve or negative.

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## ENV Variables
create a `.env` file and set a base color for the graphs(Optional)
`BASE_COLOR="#000060"`

## Usage

To start the application, navigate to the application directory and run the following command:

```bash
streamlit run app.py
```

This will start the application and provide a URL where you can access it.

To see how the exploration was done and the model was create, see the [notebooks directory](notebooks)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
