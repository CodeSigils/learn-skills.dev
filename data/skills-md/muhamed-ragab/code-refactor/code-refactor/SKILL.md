---
name: code-refactor
description: |
  Intelligent file-level refactoring for React/TypeScript projects. Handles file renaming, moving, and splitting 
  operations with intelligent analysis that automatically detects file size, component purity, and chooses the optimal 
  refactoring strategy. Uses strategy pattern to select: file splitting for large files, component extraction for impure 
  components, or simple rename/move for straightforward cases. Use this skill whenever a user wants to restructure 
  their codebase by renaming, moving, splitting files, or improving component architecture. Make sure to use this skill 
  when users mention: "rename file", "move file", "split file", "extract to new file", "restructure codebase", 
  "organize files", "refactor file structure", "make component pure", "extract logic to hook", or any similar 
  file restructuring or code quality requests.
---

# File Refactoring Skill

This skill enables Claude to perform file-level refactoring operations in React/TypeScript projects. It handles:
- **File Renaming**: Rename files and update all imports across the codebase
- **File Moving**: Move files to different directories while updating imports
- **File Splitting**: Split large files into smaller, focused modules
- **Component Optimization**: Analyze and refactor impure components to make them pure

## Core Principles

1. **Always analyze first**: Before making any changes, understand the full scope of what needs to be updated
2. **Maintain import consistency**: Every import that references the old path must be updated
3. **Preserve functionality**: The refactored code must work exactly like the original
4. **Type safety**: Ensure TypeScript types and interfaces are properly exported/imported after refactoring

---

## Strategy Pattern: Automatic Approach Selection

This skill uses a factory/strategy pattern to automatically select the best refactoring approach based on analysis.

### Analysis Workflow

When given a refactoring task, first analyze the file to determine the optimal approach:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Analyze File                              │
├─────────────────────────────────────────────────────────────────┤
│  1. Check file size (lines of code)                             │
│  2. Check if it's a React component                             │
│  3. Analyze component purity (props → JSX only)                 │
│  4. Look for inline logic that could be extracted               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Choose Strategy                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Size > 300 lines? ────YES───→ Strategy: SPLIT_FILE             │
│         │                                                        │
│         NO                                                       │
│         ▼                                                        │
│  Is React Component? ────NO───→ Strategy: RENAME/MOVE           │
│         │                                                        │
│         YES                                                      │
│         ▼                                                        │
│  Has inline state/useEffect? ────YES───→ Strategy: EXTRACT_HOOK│
│         │                                                        │
│         NO                                                       │
│         ▼                                                        │
│  Has business logic in render? ────YES───→ Strategy: PURE_COMP  │
│         │                                                        │
│         NO                                                       │
│         ▼                                                        │
│  Strategy: RENAME/MOVE                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Strategy 1: File Splitting (Large Files)

### When to Use
- File has more than 300 lines of code
- File contains multiple distinct concerns (components + hooks + types)
- User explicitly asks to split a file
- File violates Single Responsibility Principle

### How to Detect Large Files

```typescript
// Count lines in file
const lineCount = fileContent.split('\n').length;

// Threshold
const LARGE_FILE_THRESHOLD = 300;
const VERY_LARGE_FILE_THRESHOLD = 500;
```

### Splitting Strategies

**By Type of Content:**
1. **Separate Components**: If file has multiple components, extract each to its own file
2. **Separate Types**: Extract interfaces, types, and type guards to `types.ts`
3. **Separate Hooks**: Extract custom hooks to `hooks/` directory
4. **Separate Utils**: Extract utility functions to `utils/` directory

**Example Split Plan:**
```
Before: LargeComponent.tsx (450 lines)
  - CustomerTable component (150 lines)
  - CustomerRow component (50 lines)  
  - useCustomerFilters hook (80 lines)
  - CustomerType interface (20 lines)
  - Helper functions (50 lines)
  - Styles (100 lines)

After:
  - components/CustomerTable.tsx    (150 lines)
  - components/CustomerRow.tsx     (50 lines)
  - hooks/useCustomerFilters.ts    (80 lines)
  - types/Customer.ts              (20 lines)
  - utils/customerHelpers.ts       (50 lines)
  - CustomerTable.module.css       (100 lines)
```

### Steps

1. **Analyze the source file**:
   - Count lines of code
   - Identify distinct sections (components, hooks, utilities, types)
   - Determine which exports belong together
   - Identify shared dependencies between sections

2. **Plan the split**:
   - Decide on the new file structure based on content types
   - Determine what each new file will export
   - Plan the import relationships between new files
   - Consider creating barrel files (index.ts) for organized exports

3. **Create new files**:
   - Create each new file with its extracted content
   - Ensure proper exports are maintained
   - Add necessary imports within the new files

4. **Update the original file**:
   - Replace extracted content with re-exports from new files
   - Or remove extracted content entirely if fully separated

5. **Update all imports**:
   - Find all files that import from the original file
   - Update imports to point to the correct new file
   - Handle both direct imports and barrel file re-exports

6. **Verify**:
   - Run TypeScript check: `pnpm exec tsc --noEmit`
   - Run lint: `pnpm lint`
   - Check that all functionality works

---

## Strategy 2: Component Purity Analysis

### What is a Pure Component?

A **pure component** is one that:
1. Given the same props, always renders the same output
2. Does NOT have internal state (`useState`)
3. Does NOT have side effects (`useEffect`)
4. Does NOT directly mutate props or external state
5. Only computes derived data from props

**Pure Component Example:**
```tsx
// PURE - only transforms props to JSX
function CustomerRow({ customer }: CustomerRowProps) {
  return (
    <tr>
      <td>{customer.name}</td>
      <td>{customer.email}</td>
    </tr>
  );
}
```

**Impure Component Example:**
```tsx
// IMPURE - has internal state and side effects
function CustomerForm({ initialData }: CustomerFormProps) {
  const [name, setName] = useState(initialData?.name || "");
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // Side effect - fetching data
    fetchCustomer(id).then(setData);
  }, [id]);
  
  const handleSave = () => {
    // Side effect - mutations
    saveCustomer({ name, ... });
  };
  
  // ... render with form
}
```

### Signs of an Impure Component (Candidates for Refactoring)

1. **useState** - Internal state that could be managed by parent
2. **useEffect** - Side effects that could be extracted to hooks
3. **Inline business logic** - Complex computations in render that could be utilities
4. **Inline data fetching** - API calls that could be in a custom hook
5. **Inline form handling** - Form state that could use react-hook-form

### Refactoring Impure Components to Pure

#### Step 1: Extract State Management to Parent

**Before:**
```tsx
function CustomerForm({ customer }: CustomerFormProps) {
  const [name, setName] = useState(customer.name);
  const [email, setEmail] = useState(customer.email);
  // ... form submission logic
}
```

**After:**
```tsx
// Parent manages state
function CustomerFormWrapper({ customer }: CustomerFormProps) {
  const [formData, setFormData] = useState({
    name: customer.name,
    email: customer.email
  });
  
  return <CustomerForm formData={formData} onChange={setFormData} />;
}

// Pure component - receives data, returns JSX
function CustomerForm({ 
  formData, 
  onChange 
}: CustomerFormProps) {
  return (
    <form>
      <input 
        value={formData.name} 
        onChange={(e) => onChange({ ...formData, name: e.target.value })} 
      />
    </form>
  );
}
```

#### Step 2: Extract Side Effects to Custom Hooks

**Before:**
```tsx
function CustomerDetail({ customerId }: CustomerDetailProps) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(`/api/customers/${customerId}`)
      .then(res => res.json())
      .then(data => {
        setCustomer(data);
        setLoading(false);
      });
  }, [customerId]);
  
  if (loading) return <Spinner />;
  return <div>{customer?.name}</div>;
}
```

**After:**
```tsx
// Custom hook - encapsulates side effects
function useCustomer(customerId: string) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(`/api/customers/${customerId}`)
      .then(res => res.json())
      .then(data => {
        setCustomer(data);
        setLoading(false);
      });
  }, [customerId]);
  
  return { customer, loading };
}

// Pure component
function CustomerDetail({ customerId }: CustomerDetailProps) {
  const { customer, loading } = useCustomer(customerId);
  
  if (loading) return <Spinner />;
  return <div>{customer?.name}</div>;
}
```

#### Step 3: Extract Business Logic to Utils/Hooks

**Before:**
```tsx
function OrderSummary({ items }: OrderSummaryProps) {
  const total = items.reduce((sum, item) => {
    const tax = item.price * 0.15;
    const discount = item.price * (item.discount || 0);
    return sum + item.price + tax - discount;
  }, 0);
  
  const formatted = new Intl.NumberFormat('ar-EG', {
    style: 'currency',
    currency: 'EGP'
  }).format(total);
  
  return <div>Total: {formatted}</div>;
}
```

**After:**
```tsx
// utils/orders.ts
export function calculateOrderTotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => {
    const tax = item.price * 0.15;
    const discount = item.price * (item.discount || 0);
    return sum + item.price + tax - discount;
  }, 0);
}

export function formatCurrency(amount: number, locale = 'ar-EG'): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: 'EGP'
  }).format(amount);
}

// Component - now pure
function OrderSummary({ items }: OrderSummaryProps) {
  const total = calculateOrderTotal(items);
  const formatted = formatCurrency(total);
  
  return <div>Total: {formatted}</div>;
}
```

---

## Strategy 3: File Renaming

### When to Use
- User wants to rename a file (e.g., `MyComponent.tsx` → `InventoryTable.tsx`)
- User wants to change a component name and its file
- User wants to improve naming convention

### Steps

1. **Analyze the current file**:
   - Read the file content to understand its exports
   - Check what imports it has
   - Identify all named exports

2. **Find all references**:
   - Search for imports using the current filename (both with and without extensions)
   - Search for imports using the exported names
   - Check for dynamic imports and lazy loading

3. **Rename the file**:
   - Use `bash` tool to rename: `mv old-name.tsx new-name.tsx`

4. **Update all imports**:
   - For each file that imports the renamed file, update the import path
   - Keep the same import style (named, default, namespace)

5. **Verify**:
   - Run TypeScript check: `pnpm exec tsc --noEmit`
   - Run lint: `pnpm lint`
   - Check that the application still works

---

## Strategy 4: File Moving

### When to Use
- User wants to move a file to a different directory
- User wants to reorganize project structure
- User wants to group related files together

### Steps

1. **Analyze source and destination**:
   - Read the file to understand its imports/exports
   - Check if destination directory exists
   - Determine the correct relative paths after move

2. **Find all references**:
   - Search for all imports of the file from any location in the codebase
   - Check relative imports that might be affected

3. **Move the file**:
   - Create destination directory if needed: `mkdir -p dest/dir`
   - Move file: `mv source/file.tsx dest/dir/file.tsx`

4. **Update all imports**:
   - Calculate new relative paths for each importing file
   - Update import statements accordingly
   - Handle both relative (`../`) and alias (`@/`) imports

5. **Verify**:
   - Run TypeScript check
   - Run lint
   - Ensure no broken imports remain

---

## Important Patterns

### Handling Barrel Files (index.ts)
When moving or renaming files that have an `index.ts` barrel:
- Consider whether to keep the barrel file or update imports to point directly
- Update barrel exports accordingly

### React Components
When refactoring React component files:
- Update component names in the file to match the new filename (if applicable)
- Check for `displayName` properties used for React DevTools
- Update any `React.lazy()` or dynamic imports

### TypeScript Types
When splitting files with types:
- Export interfaces and types explicitly
- Update any type-only imports
- Check for circular dependency issues

### Test Files
When files have corresponding test files:
- Rename or move test files alongside the source files
- Update test imports accordingly
- Ensure test paths in `vitest.config.ts` or `tsconfig.json` still work

---

## Auto-Detection Checklist

When analyzing a file, check these indicators:

| Indicator | Strategy to Use |
|-----------|-----------------|
| File > 300 lines | SPLIT_FILE |
| Multiple components in one file | SPLIT_FILE |
| Component has `useState` + `useEffect` | EXTRACT_HOOK + PURE_COMP |
| Component has complex inline logic | EXTRACT_TO_UTILS |
| Component only renders JSX | KEEP_PURE |
| File name doesn't match content | RENAME |

---

## Verification Checklist

After any refactoring operation, always verify:

- [ ] TypeScript compiles without errors: `pnpm exec tsc --noEmit`
- [ ] Linting passes: `pnpm lint`
- [ ] Tests pass (if applicable): `pnpm test:run`
- [ ] No remaining references to old file paths
- [ ] Application builds successfully: `pnpm build`

---

## Output Format

When presenting the refactoring results to the user:

1. **Strategy Used**: Which strategy pattern was applied (Split, Extract, Rename, Move)
2. **Analysis**: Brief description of what was found (e.g., "File had 450 lines, 2 components, 1 hook")
3. **Summary**: What files were renamed/moved/split
4. **Changes Made**: List of all files modified
5. **Verification**: Results from typecheck, lint, and tests
6. **Notes**: Any important considerations or warnings

Be clear and concise. The user should understand exactly what changed and why the specific strategy was chosen.
