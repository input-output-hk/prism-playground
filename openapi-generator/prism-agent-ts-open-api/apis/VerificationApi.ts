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


import * as runtime from '../runtime';
import type {
  ErrorResponse,
  VerificationPolicy,
  VerificationPolicyInput,
  VerificationPolicyPage,
} from '../models';
import {
    ErrorResponseFromJSON,
    ErrorResponseToJSON,
    VerificationPolicyFromJSON,
    VerificationPolicyToJSON,
    VerificationPolicyInputFromJSON,
    VerificationPolicyInputToJSON,
    VerificationPolicyPageFromJSON,
    VerificationPolicyPageToJSON,
} from '../models';

export interface CreateVerificationPolicyRequest {
    verificationPolicyInput: VerificationPolicyInput;
}

export interface DeleteVerificationPolicyByIdRequest {
    id: string;
    nonce: number;
}

export interface GetVerificationPolicyByIdRequest {
    id: string;
}

export interface LookupVerificationPoliciesByQueryRequest {
    name?: string;
    offset?: number;
    limit?: number;
    order?: string;
}

export interface UpdateVerificationPolicyRequest {
    id: string;
    nonce: number;
    verificationPolicyInput: VerificationPolicyInput;
}

/**
 * 
 */
export class VerificationApi extends runtime.BaseAPI {

    /**
     * Create the new verification policy
     * Create the new verification policy
     */
    async createVerificationPolicyRaw(requestParameters: CreateVerificationPolicyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VerificationPolicy>> {
        if (requestParameters.verificationPolicyInput === null || requestParameters.verificationPolicyInput === undefined) {
            throw new runtime.RequiredError('verificationPolicyInput','Required parameter requestParameters.verificationPolicyInput was null or undefined when calling createVerificationPolicy.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/verification/policies`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: VerificationPolicyInputToJSON(requestParameters.verificationPolicyInput),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VerificationPolicyFromJSON(jsonValue));
    }

    /**
     * Create the new verification policy
     * Create the new verification policy
     */
    async createVerificationPolicy(requestParameters: CreateVerificationPolicyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VerificationPolicy> {
        const response = await this.createVerificationPolicyRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Delete the verification policy by id
     * Deleted the verification policy by id
     */
    async deleteVerificationPolicyByIdRaw(requestParameters: DeleteVerificationPolicyByIdRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<void>> {
        if (requestParameters.id === null || requestParameters.id === undefined) {
            throw new runtime.RequiredError('id','Required parameter requestParameters.id was null or undefined when calling deleteVerificationPolicyById.');
        }

        if (requestParameters.nonce === null || requestParameters.nonce === undefined) {
            throw new runtime.RequiredError('nonce','Required parameter requestParameters.nonce was null or undefined when calling deleteVerificationPolicyById.');
        }

        const queryParameters: any = {};

        if (requestParameters.nonce !== undefined) {
            queryParameters['nonce'] = requestParameters.nonce;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/verification/policies/{id}`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters.id))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Delete the verification policy by id
     * Deleted the verification policy by id
     */
    async deleteVerificationPolicyById(requestParameters: DeleteVerificationPolicyByIdRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<void> {
        await this.deleteVerificationPolicyByIdRaw(requestParameters, initOverrides);
    }

    /**
     * Get the verification policy by id
     * Fetch the verification policy by id
     */
    async getVerificationPolicyByIdRaw(requestParameters: GetVerificationPolicyByIdRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VerificationPolicy>> {
        if (requestParameters.id === null || requestParameters.id === undefined) {
            throw new runtime.RequiredError('id','Required parameter requestParameters.id was null or undefined when calling getVerificationPolicyById.');
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/verification/policies/{id}`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters.id))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VerificationPolicyFromJSON(jsonValue));
    }

    /**
     * Get the verification policy by id
     * Fetch the verification policy by id
     */
    async getVerificationPolicyById(requestParameters: GetVerificationPolicyByIdRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VerificationPolicy> {
        const response = await this.getVerificationPolicyByIdRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Lookup verification policies by `name`, and control the pagination by `offset` and `limit` parameters
     * Lookup verification policies by query
     */
    async lookupVerificationPoliciesByQueryRaw(requestParameters: LookupVerificationPoliciesByQueryRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VerificationPolicyPage>> {
        const queryParameters: any = {};

        if (requestParameters.name !== undefined) {
            queryParameters['name'] = requestParameters.name;
        }

        if (requestParameters.offset !== undefined) {
            queryParameters['offset'] = requestParameters.offset;
        }

        if (requestParameters.limit !== undefined) {
            queryParameters['limit'] = requestParameters.limit;
        }

        if (requestParameters.order !== undefined) {
            queryParameters['order'] = requestParameters.order;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/verification/policies`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VerificationPolicyPageFromJSON(jsonValue));
    }

    /**
     * Lookup verification policies by `name`, and control the pagination by `offset` and `limit` parameters
     * Lookup verification policies by query
     */
    async lookupVerificationPoliciesByQuery(requestParameters: LookupVerificationPoliciesByQueryRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VerificationPolicyPage> {
        const response = await this.lookupVerificationPoliciesByQueryRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Update the verification policy entry
     * Update the verification policy object by id
     */
    async updateVerificationPolicyRaw(requestParameters: UpdateVerificationPolicyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<VerificationPolicy>> {
        if (requestParameters.id === null || requestParameters.id === undefined) {
            throw new runtime.RequiredError('id','Required parameter requestParameters.id was null or undefined when calling updateVerificationPolicy.');
        }

        if (requestParameters.nonce === null || requestParameters.nonce === undefined) {
            throw new runtime.RequiredError('nonce','Required parameter requestParameters.nonce was null or undefined when calling updateVerificationPolicy.');
        }

        if (requestParameters.verificationPolicyInput === null || requestParameters.verificationPolicyInput === undefined) {
            throw new runtime.RequiredError('verificationPolicyInput','Required parameter requestParameters.verificationPolicyInput was null or undefined when calling updateVerificationPolicy.');
        }

        const queryParameters: any = {};

        if (requestParameters.nonce !== undefined) {
            queryParameters['nonce'] = requestParameters.nonce;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        const response = await this.request({
            path: `/verification/policies/{id}`.replace(`{${"id"}}`, encodeURIComponent(String(requestParameters.id))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: VerificationPolicyInputToJSON(requestParameters.verificationPolicyInput),
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => VerificationPolicyFromJSON(jsonValue));
    }

    /**
     * Update the verification policy entry
     * Update the verification policy object by id
     */
    async updateVerificationPolicy(requestParameters: UpdateVerificationPolicyRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<VerificationPolicy> {
        const response = await this.updateVerificationPolicyRaw(requestParameters, initOverrides);
        return await response.value();
    }

}