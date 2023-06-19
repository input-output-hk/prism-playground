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
import type { VerificationPolicy } from './VerificationPolicy';
import {
    VerificationPolicyFromJSON,
    VerificationPolicyFromJSONTyped,
    VerificationPolicyToJSON,
} from './VerificationPolicy';

/**
 * 
 * @export
 * @interface VerificationPolicyPage
 */
export interface VerificationPolicyPage {
    /**
     * 
     * @type {string}
     * @memberof VerificationPolicyPage
     */
    self: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationPolicyPage
     */
    kind: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationPolicyPage
     */
    pageOf: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationPolicyPage
     */
    next?: string;
    /**
     * 
     * @type {string}
     * @memberof VerificationPolicyPage
     */
    previous?: string;
    /**
     * 
     * @type {Array<VerificationPolicy>}
     * @memberof VerificationPolicyPage
     */
    contents?: Array<VerificationPolicy>;
}

/**
 * Check if a given object implements the VerificationPolicyPage interface.
 */
export function instanceOfVerificationPolicyPage(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "self" in value;
    isInstance = isInstance && "kind" in value;
    isInstance = isInstance && "pageOf" in value;

    return isInstance;
}

export function VerificationPolicyPageFromJSON(json: any): VerificationPolicyPage {
    return VerificationPolicyPageFromJSONTyped(json, false);
}

export function VerificationPolicyPageFromJSONTyped(json: any, ignoreDiscriminator: boolean): VerificationPolicyPage {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'self': json['self'],
        'kind': json['kind'],
        'pageOf': json['pageOf'],
        'next': !exists(json, 'next') ? undefined : json['next'],
        'previous': !exists(json, 'previous') ? undefined : json['previous'],
        'contents': !exists(json, 'contents') ? undefined : ((json['contents'] as Array<any>).map(VerificationPolicyFromJSON)),
    };
}

export function VerificationPolicyPageToJSON(value?: VerificationPolicyPage | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'self': value.self,
        'kind': value.kind,
        'pageOf': value.pageOf,
        'next': value.next,
        'previous': value.previous,
        'contents': value.contents === undefined ? undefined : ((value.contents as Array<any>).map(VerificationPolicyToJSON)),
    };
}
