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
import type { DIDDocument } from './DIDDocument';
import {
    DIDDocumentFromJSON,
    DIDDocumentFromJSONTyped,
    DIDDocumentToJSON,
} from './DIDDocument';
import type { DIDDocumentMetadata } from './DIDDocumentMetadata';
import {
    DIDDocumentMetadataFromJSON,
    DIDDocumentMetadataFromJSONTyped,
    DIDDocumentMetadataToJSON,
} from './DIDDocumentMetadata';
import type { DIDResolutionMetadata } from './DIDResolutionMetadata';
import {
    DIDResolutionMetadataFromJSON,
    DIDResolutionMetadataFromJSONTyped,
    DIDResolutionMetadataToJSON,
} from './DIDResolutionMetadata';

/**
 * 
 * @export
 * @interface DIDResolutionResult
 */
export interface DIDResolutionResult {
    /**
     * The JSON-LD context for the DID resolution result.
     * @type {string}
     * @memberof DIDResolutionResult
     */
    context: string;
    /**
     * 
     * @type {DIDDocument}
     * @memberof DIDResolutionResult
     */
    didDocument?: DIDDocument;
    /**
     * 
     * @type {DIDDocumentMetadata}
     * @memberof DIDResolutionResult
     */
    didDocumentMetadata: DIDDocumentMetadata;
    /**
     * 
     * @type {DIDResolutionMetadata}
     * @memberof DIDResolutionResult
     */
    didResolutionMetadata: DIDResolutionMetadata;
}

/**
 * Check if a given object implements the DIDResolutionResult interface.
 */
export function instanceOfDIDResolutionResult(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "context" in value;
    isInstance = isInstance && "didDocumentMetadata" in value;
    isInstance = isInstance && "didResolutionMetadata" in value;

    return isInstance;
}

export function DIDResolutionResultFromJSON(json: any): DIDResolutionResult {
    return DIDResolutionResultFromJSONTyped(json, false);
}

export function DIDResolutionResultFromJSONTyped(json: any, ignoreDiscriminator: boolean): DIDResolutionResult {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'context': json['@context'],
        'didDocument': !exists(json, 'didDocument') ? undefined : DIDDocumentFromJSON(json['didDocument']),
        'didDocumentMetadata': DIDDocumentMetadataFromJSON(json['didDocumentMetadata']),
        'didResolutionMetadata': DIDResolutionMetadataFromJSON(json['didResolutionMetadata']),
    };
}

export function DIDResolutionResultToJSON(value?: DIDResolutionResult | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        '@context': value.context,
        'didDocument': DIDDocumentToJSON(value.didDocument),
        'didDocumentMetadata': DIDDocumentMetadataToJSON(value.didDocumentMetadata),
        'didResolutionMetadata': DIDResolutionMetadataToJSON(value.didResolutionMetadata),
    };
}

