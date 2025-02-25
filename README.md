# FlexStack(R) Community Edition

<!--<img src="doc/img/logo.png" alt="V2X Flex Stack" width="200"/>--> <img src="doc/img/i2cat_logo.png" alt="i2CAT Logo" width="200"/>


# Short description
FlexStack(R) is a software library implementing the ETSI C-ITS protocol stack.  Its aim is to facilitate and accelerate the development and integration of software applications on vehicles, vulnerable road users (VRU), and roadside infrastructure that requires the exchange of V2X messages (compliant with ETSI standards) with other actors of the V2X ecosystem.

# Pre-requisites

## Supported Operating Systems

This library can run on any system that supports Python 3.8 or higher. 

It's important to remark that depending on the Access Technologies used, the library may require additional dependencies. For example, to use C-V2X with Qualcomm based solutions the library requires the cross-compilation of the "C-V2X Link Layer" that enables the usage of C-V2X directly by this message library.

## Dependencies

All dependecies can be found in the `requirements.txt` file. To install them, run the following command:

```
pip install -r requirements.txt
```

On the Access Layer, the dependencies depends on the Access Technology used. Specific tutorials and examples can be found elsewhere.

## Build tools

The library is built using Python. To build the library, run the following command:

```
python -m build
```
It requires the `setuptools` and `wheel` packages. If they are not installed, they can be installed using the following command:

```
pip install build setuptools wheel
```

## Other dependencies

Depending on the specific use case or application intended there might be additional dependencies. For example, there might be considered the usage of MQTT
broker to send and receive messages from the V2X library.

# Installation

Library can be easily installed using the following command:

```
pip install v2xflexstack
```

<!--# Technical description (very basic)
Technical overview of the software, for example:
If this is a library, code snippets showing how to use the library in another application.
Software architecture overview 
External dependencies-->

## Developers

- Jordi Marias-i-Parella (jordi.marias@i2cat.net)
- Daniel Ulied Guevara (daniel.ulied@i2cat.net)
- Adrià Pons Serra (adria.pons@i2cat.net)
- Marc Codina Bartomeus (marc.codina@i2cat.net)



# Source

This code has been developed within the following research and innovation projects:
- **CARAMEL** (Grant Agreement No. 833611) – Funded under the Horizon 2020 programme, focusing on cybersecurity for connected and autonomous vehicles.
- **PLEDGER** (Grant Agreement No. 871536) – A Horizon 2020 project aimed at edge computing solutions to improve performance and security.
- **CODECO** (Grant Agreement No. 101092696) – A Horizon Europe initiative addressing cooperative and connected mobility.
- **SAVE-V2X** (Grant Agreement No. ACE05322000044) – Focused on V2X communication for vulnerable road user safety, and funded by ACCIO.

# Copyright
This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT). 

FlexStack is a registered trademark of i2CAT. Unauthorized use is strictly prohibited. 

i2CAT is a __non-profit research and innovation centre that__ promotes mission-driven knowledge to solve business challenges, co-create solutions with a transformative impact, empower citizens through open and participative digital social innovation with territorial capillarity, and promote pioneering and strategic initiatives. i2CAT __aims to transfer__ research project results to private companies in order to create social and economic impact via the out-licensing of intellectual property and the creation of spin-offs. Find more information of i2CAT projects and IP rights at https://i2cat.net/tech-transfer/ 

# License

This code is licensed under the terms of the AGPL. Information about the license can be located at https://www.gnu.org/licenses/agpl-3.0.html. 

Please, refer to FlexStack Community Edition as a dependence of your works. 

If you find that this license doesn't fit with your requirements regarding the use, distribution or redistribution of our code for your specific work, please, don’t hesitate to contact the intellectual property managers in i2CAT at the following address: techtransfer@i2cat.net Also, in the following page you’ll find more information about the current commercialization status or other licensees: Under Development.

# Attributions

Attributions of Third Party Components of this work:
- `asn1tools` Version 0.165.0 -  Imported python library - https://asn1tools.readthedocs.io/en/latest/ - MIT license
- `python-dateutil` Version 2.8.2 - Imported python library - https://pypi.org/project/python-dateutil/ - dual license - either Apache 2.0 License or the BSD 3-Clause License.
- `tinydb` Version 4.7.1- Imported python library - https://tinydb.readthedocs.io/en/latest/ - MIT license
- `ecdsa` Version 0.18.0 - Imported python library - https://pypi.org/project/ecdsa/ - MIT license

# External links

https://www.flexstack.eu

