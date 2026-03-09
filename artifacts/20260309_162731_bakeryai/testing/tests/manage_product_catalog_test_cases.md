# Test Case Document - US-001: Manage Product Catalog

## 1. Objective
The objective of this test case is to verify that the bakery staff member can perform the following actions in the manage_product_catalog module:
- Add a new product to the catalog
- Edit an existing product's details
- Delete a product from the catalog

## 2. Preconditions
- The manage_product_catalog module is accessible to the bakery staff member.
- The bakery staff member is logged in to the system.
- The product catalog is not full and has available slots for adding new products.

## 3. Test Cases

### Add New Product
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC001 | Valid product details are entered and saved | New product is added to the catalog with all necessary details |
| TC002 | Invalid product details are entered | Error message is displayed and product is not added to the catalog |
| TC003 | Product name is left blank | Error message is displayed and product is not added to the catalog |
| TC004 | Product price is left blank | Error message is displayed and product is not added to the catalog |
| TC005 | Product image file is too large | Error message is displayed and product is not added to the catalog |
| TC006 | Product image file format is not supported | Error message is displayed and product is not added to the catalog |

### Edit Product
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC007 | Valid product details are edited and saved | Product details are updated in the catalog |
| TC008 | Invalid product details are entered | Error message is displayed and product details are not updated |
| TC009 | Product name is left blank | Error message is displayed and product details are not updated |
| TC010 | Product price is left blank | Error message is displayed and product details are not updated |
| TC011 | Product image file is too large | Error message is displayed and product details are not updated |
| TC012 | Product image file format is not supported | Error message is displayed and product details are not updated |

### Delete Product
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC013 | A valid product is deleted | Product is removed from the catalog |
| TC014 | An invalid product is attempted to be deleted | Error message is displayed and product is not deleted |
| TC015 | Multiple products are attempted to be deleted at once | Error message is displayed and no products are deleted |

## 4. Exit Criteria
- All test cases have passed
- The manage_product_catalog module functions correctly and efficiently
- The bakery staff member can add, edit, and delete products from the catalog as required.