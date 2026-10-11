Feature: The Product Catalog Service
    As a store manager
    I need to manage products
    So that I can maintain the product catalog

Background:
    Given the following products
        | name    | description       | price | available | category  |
        | Hat     | A red fedora      | 59.95 | True      | CLOTHS    |
        | Shoes   | Running shoes     | 29.99 | False     | CLOTHS    |
        | Big Mac | A tasty burger    | 3.99  | True      | FOOD      |
        | Sheets  | Bed sheets        | 39.99 | True      | HOUSEWARES |

Scenario: Create a product
    When I visit the "Home Page"
    And I set the "Name" to "New Product"
    And I set the "Description" to "Created through the browser"
    And I select "True" in the "Available" dropdown
    And I select "Tools" in the "Category" dropdown
    And I set the "Price" to "12.50"
    And I press the "Create" button
    Then I should see "New Product" in the "Name" field
    
Scenario: Read a product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Hat" in the "Name" field
    And I should see "A red fedora" in the "Description" field
    And the "Available" dropdown should be set to "True"
    And the "Category" dropdown should be set to "Cloths"
    And I should see "59.95" in the "Price" field

Scenario: Update a product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    When I copy the "Id" field
    And I set the "Name" to "Fedora"
    And I press the "Update" button
    Then I should see the message "Product has been Updated!"
    When I press the "Clear" button
    And I set the "Name" to "Fedora"
    And I press the "Search" button
    Then I should see "Fedora" in the results
    And I should not see "Hat" in the results

Scenario: Delete a product
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    When I copy the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should not see "Hat" in the results

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

Scenario: Search for products by category
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "Food" in the "Category" dropdown
    And I press the "Search" button
    Then I should see "Big Mac" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Sheets" in the results

Scenario: Search for products by availability
    When I visit the "Home Page"
    And I press the "Clear" button
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Shoes" in the results

Scenario: Search for products by name
    When I visit the "Home Page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results