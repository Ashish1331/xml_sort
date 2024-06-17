import xml.etree.ElementTree as ET

def sort_index_parameters(target_product, reference_product):
    # Create a dictionary to store the index parameters of reference.xml
    reference_index_params = {param.find('name').text: param for param in reference_product.findall('index_parameter')}
    
    # Sort the index parameters of target.xml based on the order specified in reference.xml
    sorted_index_params = []
    for param in reference_product.findall('index_parameter'):
        name = param.find('name').text
        if name in reference_index_params:
            target_param = target_product.find(f"./index_parameter[name='{name}']")
            if target_param is not None:
                sorted_index_params.append(target_param)
            else:
                # If the index parameter is missing in target_product, add it from reference_product
                sorted_index_params.append(param)
    
    # Clear existing index parameters in target_product
    for param in target_product.findall('index_parameter'):
        target_product.remove(param)
    
    # Add the sorted index parameters to target_product
    for param in sorted_index_params:
        target_product.append(param)

def main():
    # Parse the reference.xml file
    reference_tree = ET.parse('reference.xml')
    reference_root = reference_tree.getroot()

    # Parse the target.xml file
    target_tree = ET.parse('target.xml')
    target_root = target_tree.getroot()

    # Create a dictionary to store the elements of target.xml
    target_dict = {elem.find('id').text: elem for elem in target_root.findall('.//product')}

    # Sort the <product> elements in target.xml according to their IDs as specified in reference.xml
    sorted_products = []
    for reference_product in reference_root.findall('.//product'):
        product_id = reference_product.find('id').text
        target_product = target_dict[product_id]
        sort_index_parameters(target_product, reference_product)
        sorted_products.append(target_product)

    # Create a new XML structure with the sorted <product> elements
    sorted_target_root = ET.Element(target_root.tag)
    for product in sorted_products:
        sorted_target_root.append(product)

    # Write the sorted XML content to a new file
    sorted_target_tree = ET.ElementTree(sorted_target_root)
    sorted_target_tree.write('sorted_target.xml', encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    main()
