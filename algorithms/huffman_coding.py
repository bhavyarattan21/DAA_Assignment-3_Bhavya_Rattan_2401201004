"""
Data Compression Module: Huffman Coding Algorithm
Greedy Strategy: Frequency-based Minimum Priority Queue Merging (Prefix-Free Codes)
Time Complexity: O(n log n) where n is distinct characters
Space Complexity: O(n)
Author: Bhavya Rattan (Roll No: 2401201004)
"""

import heapq
from collections import Counter
from typing import Dict, Tuple, Optional


class Node:
    """Represents a node in the Huffman Tree."""
    def __init__(self, char: Optional[str], freq: int, left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: 'Node') -> bool:
        # Min-heap comparison based on frequency
        return self.freq < other.freq

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_huffman_tree(text: str) -> Optional[Node]:
    """Builds the optimal Huffman Tree using min-heap priority queue."""
    if not text:
        return None

    # Count character frequencies
    frequency = Counter(text)

    # Initialize min-heap with leaf nodes for all distinct characters
    heap = [Node(char=ch, freq=freq) for ch, freq in frequency.items()]
    heapq.heapify(heap)

    # Handle edge case where text contains only one unique character
    if len(heap) == 1:
        single = heapq.heappop(heap)
        return Node(char=None, freq=single.freq, left=single, right=None)

    # Greedily merge two nodes with the lowest frequencies
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(char=None, freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]  # Root of the Huffman Tree


def generate_codes(node: Optional[Node], prefix: str = "", codebook: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Traverses Huffman tree to generate variable-length prefix-free binary codes."""
    if codebook is None:
        codebook = {}
    if node is None:
        return codebook

    if node.is_leaf():
        codebook[node.char] = prefix if prefix else "0"
        return codebook

    if node.left:
        generate_codes(node.left, prefix + "0", codebook)
    if node.right:
        generate_codes(node.right, prefix + "1", codebook)

    return codebook


def huffman_encode(text: str) -> Tuple[str, Dict[str, str], Dict[str, int], Dict[str, float]]:
    """
    Encodes text using Huffman Coding and calculates complete compression statistics.
    
    Returns:
        encoded_bits: The compressed binary string.
        codebook: Mapping of character -> binary code.
        frequencies: Character frequency counts.
        stats: Detailed statistics dictionary.
    """
    if not text:
        return "", {}, {}, {"original_bits": 0, "compressed_bits": 0, "ratio": 0.0, "savings": 0.0}

    root = build_huffman_tree(text)
    codebook = generate_codes(root)
    frequencies = dict(Counter(text))

    encoded_bits = "".join(codebook[ch] for ch in text)
    original_bits = len(text) * 8  # Standard ASCII 8 bits per character
    compressed_bits = len(encoded_bits)
    compression_ratio = (compressed_bits / original_bits) if original_bits > 0 else 0.0
    space_savings = (1.0 - compression_ratio) * 100.0 if original_bits > 0 else 0.0
    avg_code_length = (compressed_bits / len(text)) if len(text) > 0 else 0.0

    stats = {
        "original_chars": len(text),
        "distinct_chars": len(frequencies),
        "original_bits": original_bits,
        "compressed_bits": compressed_bits,
        "compression_ratio": compression_ratio,
        "space_savings_percent": space_savings,
        "avg_code_length": avg_code_length,
    }

    return encoded_bits, codebook, frequencies, stats


def huffman_decode(encoded_bits: str, root: Node) -> str:
    """Decodes the binary bitstream back into the original text string."""
    if not encoded_bits or not root:
        return ""

    decoded_chars = []
    curr = root

    for bit in encoded_bits:
        if bit == "0":
            curr = curr.left if curr.left else curr
        else:
            curr = curr.right if curr.right else curr

        if curr.is_leaf():
            decoded_chars.append(curr.char)
            curr = root

    return "".join(decoded_chars)


if __name__ == "__main__":
    sample_text = "abracadabra"
    bits, codes, freqs, statistics = huffman_encode(sample_text)
    print(f"--- Huffman Coding Results for '{sample_text}' ---")
    print("Character Frequencies:", freqs)
    print("Huffman Codebook:", codes)
    print("Encoded Bitstream:", bits)
    print(f"Original Bits: {statistics['original_bits']} | Compressed Bits: {statistics['compressed_bits']}")
    print(f"Compression Ratio: {statistics['compression_ratio']:.2%} | Space Savings: {statistics['space_savings_percent']:.2f}%")
    
    # Verify lossless decoding
    tree_root = build_huffman_tree(sample_text)
    decoded = huffman_decode(bits, tree_root)
    print("Decoded String:", decoded)
    assert decoded == sample_text, "Decoding failed!"
    print("Lossless decompression verified successfully!")
