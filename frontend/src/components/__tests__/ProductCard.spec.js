import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import ProductCard from '../ProductCard.vue'
import ButtonDark from '../ButtonDark.vue'

describe('ProductCard', () => {
  const mockProduct = {
    id: 1,
    title: 'Test Product',
    category_name: 'Category A',
    // image: 'https://example.com/image.jpg',
  }

  it('renders product information correctly', () => {
    const wrapper = mount(ProductCard, {
      props: {
        product: mockProduct,
      },
      global: {
        components: {
          ButtonDark,
        },
      },
    })

    expect(wrapper.text()).toContain('Test Product')
    expect(wrapper.text()).toContain('Category A')
    // expect(wrapper.find('img').attributes('src')).toBe()
    // expect(wrapper.find('img').attributes('alt')).toBe('Test Product')
  })

  it('displays fallback emoji when product has no image', () => {
    const productWithoutImage = {
      ...mockProduct,
      image: null,
    }

    const wrapper = mount(ProductCard, {
      props: {
        product: productWithoutImage,
      },
    })

    expect(wrapper.text()).toContain('📦')
    expect(wrapper.find('img').exists()).toBe(false)
  })

  it('emits view-details event when details button is clicked on desktop', async () => {
    // Mock window.innerWidth for desktop
    global.innerWidth = 1200

    const wrapper = mount(ProductCard, {
      props: {
        product: mockProduct,
      },
      global: {
        components: {
          ButtonDark,
        },
      },
    })

    const button = wrapper.findComponent(ButtonDark)
    await button.trigger('click')

    expect(wrapper.emitted('view-details')).toBeTruthy()
    expect(wrapper.emitted('view-details')[0]).toEqual([mockProduct.id])
  })

  it('emits view-details event when card is clicked on mobile', async () => {
    // Mock window.innerWidth for mobile
    global.innerWidth = 500

    // Trigger the updateClickable logic
    const wrapper = mount(ProductCard, {
      props: {
        product: mockProduct,
      },
    })

    await wrapper.vm.$nextTick()
    await wrapper.find('div').trigger('click')

    expect(wrapper.emitted('view-details')).toBeTruthy()
    expect(wrapper.emitted('view-details')[0]).toEqual([mockProduct.id])
  })

  it('does not emit event when card is clicked on desktop', async () => {
    // Mock window.innerWidth for desktop
    global.innerWidth = 1200

    const wrapper = mount(ProductCard, {
      props: {
        product: mockProduct,
      },
    })

    await wrapper.vm.$nextTick()
    const mainDiv = wrapper.find('[class*="flex h-full"]')
    await mainDiv.trigger('click')

    expect(wrapper.emitted('view-details')).toBeFalsy()
  })
})
