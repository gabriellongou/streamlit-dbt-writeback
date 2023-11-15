# Streamlit dbt BigQuery Application Repo

Welcome to the Streamlit dbt BigQuery application repository. This repository contains all the necessary resources and instructions for building a Streamlit application that leverages dbt and Google BigQuery.

## Overview

This application demonstrates an approach using Streamlit, an open-source Python framework. This repo focuses on exploiting Streamlit's "writeback" capabilities, especially in the context of high computing needs.

## Prerequisites

Before diving into this application, ensure that:

- You have an established technical stack (BigQuery, dbt, etc.).
- You aim to build a simulation application for a specific use case, intended for not a too large amount of users.
- Your use case necessitates high computing power for each refresh, justifying the use of BigQuery (OLAP) as the execution backend.

## Architecture

The architecture of this application integrates the following components:

- **BigQuery**: Serves as the OLAP backend for high-performance computing.
- **dbt**: Manages data transformations and workflow (DAGs).
- **Streamlit**: Provides the frontend interface, featuring the new `st.data_editor` function for enhanced interactivity.
- 
![Image1](https://github.com/gabriellongou/streamlit-dbt-writeback/assets/100798152/1ebd5877-b329-4196-9eda-3914e25759ed)

## Getting Started

1. **Read the Medium Article**: For an in-depth understanding, start by reading the accompanying Medium article about this application.
2. **Clone the Repository**: Download or clone this repository to your local machine.
3. **Follow the Step-by-Step Guide**: The repository includes a detailed guide to building your first draft of an application that combines writeback and visualization using Streamlit.

## Contributing

Your contributions are welcome! If you have suggestions or improvements, feel free to fork this repository and submit your pull requests.

## License

This project is licensed under [add your license here]. Please see the [LICENSE](LICENSE.md) file for more details.

---

For more information, questions, or feedback, please contact the repository maintainers.

Happy coding!
