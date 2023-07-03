/* tslint:disable */
/* eslint-disable */
/**
 * Prism Agent
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface IssueCredentialRecord
 */
export interface IssueCredentialRecord {
    /**
     * The identifier (e.g DID) of the subject to which the verifiable credential will be issued.
     * @type {string}
     * @memberof IssueCredentialRecord
     */
    subjectId?: string;
    /**
     * The validity period in seconds of the verifiable credential that will be issued.
     * @type {number}
     * @memberof IssueCredentialRecord
     */
    validityPeriod?: number;
    /**
     * The claims that will be associated with the issued verifiable credential.
     * @type {any}
     * @memberof IssueCredentialRecord
     */
    claims: any | null;
    /**
     * Specifies whether or not the credential should be automatically generated and issued when receiving the `CredentialRequest` from the holder. If set to `false`, a manual approval by the issuer via API call will be required for the VC to be issued.
     * @type {boolean}
     * @memberof IssueCredentialRecord
     */
    automaticIssuance?: boolean;
    /**
     * The unique identifier of the issue credential record.
     * @type {string}
     * @memberof IssueCredentialRecord
     */
    recordId: string;
    /**
     * The date and time when the issue credential record was created.
     * @type {Date}
     * @memberof IssueCredentialRecord
     */
    createdAt: Date;
    /**
     * The date and time when the issue credential record was last updated.
     * @type {Date}
     * @memberof IssueCredentialRecord
     */
    updatedAt?: Date;
    /**
     * The role played by the Prism agent in the credential issuance flow.
     * @type {string}
     * @memberof IssueCredentialRecord
     */
    role: string;
    /**
     * The current state of the issue credential protocol execution.
     * @type {string}
     * @memberof IssueCredentialRecord
     */
    protocolState: string;
    /**
     * The base64-encoded JWT verifiable credential that has been sent by the issuer.
     * @type {string}
     * @memberof IssueCredentialRecord
     */
    jwtCredential?: string;
    /**
     * Issuer DID of the verifiable credential object.
     * @type {string}
     * @memberof IssueCredentialRecord
     */
    issuingDID?: string;
}

/**
 * Check if a given object implements the IssueCredentialRecord interface.
 */
export function instanceOfIssueCredentialRecord(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "claims" in value;
    isInstance = isInstance && "recordId" in value;
    isInstance = isInstance && "createdAt" in value;
    isInstance = isInstance && "role" in value;
    isInstance = isInstance && "protocolState" in value;

    return isInstance;
}

export function IssueCredentialRecordFromJSON(json: any): IssueCredentialRecord {
    return IssueCredentialRecordFromJSONTyped(json, false);
}

export function IssueCredentialRecordFromJSONTyped(json: any, ignoreDiscriminator: boolean): IssueCredentialRecord {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'subjectId': !exists(json, 'subjectId') ? undefined : json['subjectId'],
        'validityPeriod': !exists(json, 'validityPeriod') ? undefined : json['validityPeriod'],
        'claims': json['claims'],
        'automaticIssuance': !exists(json, 'automaticIssuance') ? undefined : json['automaticIssuance'],
        'recordId': json['recordId'],
        'createdAt': (new Date(json['createdAt'])),
        'updatedAt': !exists(json, 'updatedAt') ? undefined : (new Date(json['updatedAt'])),
        'role': json['role'],
        'protocolState': json['protocolState'],
        'jwtCredential': !exists(json, 'jwtCredential') ? undefined : json['jwtCredential'],
        'issuingDID': !exists(json, 'issuingDID') ? undefined : json['issuingDID'],
    };
}

export function IssueCredentialRecordToJSON(value?: IssueCredentialRecord | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'subjectId': value.subjectId,
        'validityPeriod': value.validityPeriod,
        'claims': value.claims,
        'automaticIssuance': value.automaticIssuance,
        'recordId': value.recordId,
        'createdAt': (value.createdAt.toISOString()),
        'updatedAt': value.updatedAt === undefined ? undefined : (value.updatedAt.toISOString()),
        'role': value.role,
        'protocolState': value.protocolState,
        'jwtCredential': value.jwtCredential,
        'issuingDID': value.issuingDID,
    };
}

