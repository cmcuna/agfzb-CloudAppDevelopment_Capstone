const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const authenticator = new IamAuthenticator({
    apikey: "ryC7o8JymgX_u7rphRscO0AWUIOT3i93ohLKA4bfGonk"
});

const service = new CloudantV1({
    authenticator: authenticator
});

service.setServiceUrl('https://19a9416e-75db-496f-9156-b7fcb658e1af-bluemix.cloudantnosqldb.appdomain.cloud');
console.log("authenticated conn...")

const service1 = CloudantV1.newInstance({});

service1.getAllDbs().then(response => {
  console.log(response.result);
});

