# Netio Integration for Home Assistant

This custom Home Assistant integration is designed for Netio products that expose a JSON API. It allows you to control Netio outlets as on/off switches via Home Assistant.

## Features

- **Simple Configuration:**  
  Configure your Netio device (IP, port, username, and password) through the Home Assistant UI.
  
- **Automatic Discovery:**  
  Automatically discover available outlets on your Netio device.
  
- **On/Off Control:**  
  Create Home Assistant switch entities for each discovered outlet.  
  **Note:** Only basic on/off switch functionality is supported at this time.

## Installation

### Via HACS

1. In Home Assistant, open **HACS > Integrations > Explore & Add Repositories**.
2. Search for **Netio Integration** and install it.
3. Restart Home Assistant.
4. Configure the integration via the Home Assistant UI.

### Manual Installation

1. Clone or download this repository.
2. Copy the `custom_components/netio` folder into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.
4. Configure the integration via the Home Assistant UI by entering your Netio device details.

## Configuration

When you set up the integration, you will be prompted to provide:

- **IP Address:** The IP address of your Netio device.
- **Port:** The port number (default is often `1234` or as specified by your device).
- **Username:** Your Netio device username.
- **Password:** Your Netio device password.

The integration uses these details to connect to your Netio device, automatically discovers the available outlets via its JSON API, and creates corresponding switch entities in Home Assistant.

## Supported Devices

This integration is built specifically for Netio products with a JSON API.  
**Current Support:**  
- On/Off switch control for each discovered outlet.

## Future Improvements

- Support for additional outlet functionalities
- Enhanced state management and error handling
- Extended configuration options and device features

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to fork this repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

