# 0002 - Data Storage

Date: 2022-12-08

## Context:

The application needs to store data. The data can be stored in a cloud database or in local files. It has to be easily accessable from all kinds of devices, but it has to be stored in a way that is secure. 

If the data is stored in files then a local server should be created to make the data accessable from all devices. Also the data should be encrypted to make it secure and authentication should be added to make sure that only authorized users can access the data.

If the data is stored in a cloud database then the data is accessable from all devices and it is secure. The authentication is handled by the cloud provider. However, the cloud database is not free most of the time.

## Decision:

The data will be stored in Googlesheets as a cloud database.

## Consequences:

- The data is stored in a cloud database, so it is accessable from all devices

- The data is stored in a secure way, because the authentication is handled by Google